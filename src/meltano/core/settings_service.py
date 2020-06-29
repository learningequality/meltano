import os
import sqlalchemy
import logging
from typing import Iterable, Dict, List
from enum import Enum
import re

from meltano.core.utils import (
    find_named,
    setting_env,
    NotFound,
    truthy,
    flatten,
    set_at_path,
    pop_at_path,
)
from .setting_definition import SettingDefinition
from .setting import Setting
from .plugin_discovery_service import PluginDiscoveryService
from .config_service import ConfigService
from .error import Error


class SettingMissingError(Error):
    """Occurs when a setting is missing."""

    def __init__(self, name: str):
        super().__init__(f"Cannot find setting {name}")


class SettingValueSource(str, Enum):
    CONFIG_OVERRIDE = "config_override"  # 0
    ENV = "env"  # 1
    MELTANO_YML = "meltano_yml"  # 2
    DB = "db"  # 3
    DEFAULT = "default"  # 4


class SettingValueStore(str, Enum):
    MELTANO_YML = "meltano_yml"
    DB = "db"


# sentinel value to use to prevent leaking sensitive data
REDACTED_VALUE = "(redacted)"


class SettingsService:
    def __init__(
        self,
        project,
        session=None,
        plugin_discovery_service: PluginDiscoveryService = None,
        config_service: ConfigService = None,
        show_hidden=True,
        path_prefix=[],
        env_override={},
        config_override={},
    ):
        self.project = project
        self.session = session

        self.discovery_service = plugin_discovery_service or PluginDiscoveryService(
            project
        )
        self.config_service = config_service or ConfigService(project)

        self.show_hidden = show_hidden
        self.path_prefix = path_prefix
        self.name_prefix = ".".join([*self.path_prefix, ""])

        self.env_override = env_override
        self.config_override = config_override

        self._env = None

    def with_env_override(self, env_override):
        return self.__class__(
            *self._args,
            **self._kwargs,
            env_override={**self.env_override, **env_override},
            config_override=self.config_override,
        )

    def with_config_override(self, config_override):
        return self.__class__(
            *self._args,
            **self._kwargs,
            env_override=self.env_override,
            config_override={**self.config_override, **config_override},
        )

    @classmethod
    def is_kind_redacted(cls, kind) -> bool:
        return kind in ("password", "oauth")

    @classmethod
    def unredact(cls, values: dict) -> Dict:
        """
        Removes any redacted values in a dictionary.
        """

        return {k: v for k, v in values.items() if v != REDACTED_VALUE}

    @property
    def env(self):
        if not self._env:
            self._env = {**os.environ, **self.env_override}

        return self._env

    def config_with_sources(
        self, sources: List[SettingValueSource] = None, redacted=False
    ):
        setting_names = [setting.name for setting in self.definitions()]

        flat_config = flatten(self._current_config, "dot")
        setting_names.extend(flat_config.keys())

        config = {}
        for name in setting_names:
            if self.name_prefix and not name.startswith(self.name_prefix):
                continue

            value, source = self.get_value(name, redacted=redacted)
            if sources and source not in sources:
                continue

            config[name] = {"value": value, "source": source}

        return config

    def as_config(self, *args, **kwargs) -> Dict:
        full_config = self.config_with_sources(*args, **kwargs)

        return {key: config["value"] for key, config in full_config.items()}

    def as_env(self, sources: List[SettingValueSource] = None) -> Dict[str, str]:
        env = {}

        for setting in self.definitions():
            if self.name_prefix and not setting.name.startswith(self.name_prefix):
                continue

            value, source = self.get_value(setting.name)
            if sources and source not in sources:
                logging.debug(f"Setting {setting.name} is not in sources: {sources}.")
                continue

            if value is None:
                continue

            env_key = self.setting_env(setting)
            env[env_key] = str(value)

        return env

    def set(self, path: List[str], value, store=SettingValueStore.MELTANO_YML):
        if isinstance(path, str):
            path = [path]

        path = [*self.path_prefix, *path]

        name = ".".join(path)

        if value == REDACTED_VALUE:
            return

        try:
            setting_def = self.find_setting(name)
        except SettingMissingError:
            setting_def = None

        if setting_def:
            value = self.cast_value(setting_def, value)

            env_key = self.setting_env(setting_def)

            if env_key in self.env:
                logging.warning(f"Setting `{name}` is currently set via ${env_key}.")

        def meltano_yml_setter():
            config = self._current_config

            if value is None:
                config.pop(name, None)
                pop_at_path(config, name, None)
                pop_at_path(config, path, None)
            else:
                if len(path) > 1:
                    config.pop(name, None)

                if name.split(".") != path:
                    pop_at_path(config, name, None)

                set_at_path(config, path, value)

            self._update_config()
            return True

        def db_setter():
            if not self.session:
                return None

            if value is None:
                self.session.query(Setting).filter_by(
                    namespace=self._db_namespace, name=name
                ).delete()
            else:
                setting = Setting(
                    namespace=self._db_namespace, name=name, value=value, enabled=True
                )
                self.session.merge(setting)

            self.session.commit()
            return True

        config_setters = {
            SettingValueStore.MELTANO_YML: meltano_yml_setter,
            SettingValueStore.DB: db_setter,
        }

        if not config_setters[store]():
            return

        return value

    def unset(self, path: List[str], store=SettingValueStore.MELTANO_YML):
        return self.set(path, None, store)

    def reset(self, store=SettingValueStore.MELTANO_YML):
        def meltano_yml_resetter():
            config = self._current_config

            if self.path_prefix:
                pop_at_path(config, self.path_prefix, None)
                for key in config.keys():
                    if key.startswith(self.name_prefix):
                        config.pop(key)
            else:
                config.clear()

            self._update_config()
            return True

        def db_resetter():
            if not self.session:
                return None

            settings = self.session.query(Setting).filter_by(
                namespace=self._db_namespace
            )
            if self.name_prefix:
                settings.filter(Setting.name.like(f"{self.name_prefix}%")).delete()
            else:
                settings.delete()

            self.session.commit()
            return True

        config_resetters = {
            SettingValueStore.MELTANO_YML: meltano_yml_resetter,
            SettingValueStore.DB: db_resetter,
        }

        if not config_resetters[store]():
            return False

        return True

    def find_setting(self, name: str) -> SettingDefinition:
        try:
            return find_named(self.definitions(), name)
        except NotFound as err:
            raise SettingMissingError(name) from err

    def definitions(self) -> Iterable[Dict]:
        settings = []
        for s in self._definitions:
            if s.kind == "hidden" and not self.show_hidden:
                continue
            if self.name_prefix and not s.name.startswith(self.name_prefix):
                continue

            settings.append(s)
        return settings

    def _current_config(self):
        return NotImplementedError

    def _definitions(self):
        return NotImplementedError

    def _env_namespace(self):
        return NotImplementedError

    def _db_namespace(self):
        return NotImplementedError

    def _update_config(self):
        return NotImplementedError

    def setting_env(self, setting_def):
        return setting_def.env or setting_env(self._env_namespace, setting_def.name)

    def cast_value(self, setting_def, value):
        if isinstance(value, str) and setting_def.kind == "boolean":
            value = truthy(value)

        return value

    def get_value(self, name: str, redacted=False):
        try:
            setting_def = self.find_setting(name)
        except SettingMissingError:
            setting_def = None

        def config_override_getter():
            try:
                return self.config_override[name]
            except KeyError:
                return None

        def env_getter():
            if not setting_def:
                return None

            env_key = self.setting_env(setting_def)

            try:
                return self.env[env_key]
            except KeyError:
                return None
            else:
                logging.debug(
                    f"Found ENV variable {env_key} for {self._env_namespace}:{name}"
                )

        def meltano_yml_getter():
            try:
                flat_config = flatten(self._current_config, "dot")
                value = flat_config[name]
                return self.expand_env_vars(value)
            except KeyError:
                return None

        def db_getter():
            if not self.session:
                return None

            try:
                return (
                    self.session.query(Setting)
                    .filter_by(namespace=self._db_namespace, name=name, enabled=True)
                    .one()
                    .value
                )
            except sqlalchemy.orm.exc.NoResultFound:
                return None

        def default_getter():
            if not setting_def:
                return None
            return self.expand_env_vars(setting_def.value)

        config_getters = {
            SettingValueSource.CONFIG_OVERRIDE: config_override_getter,
            SettingValueSource.ENV: env_getter,
            SettingValueSource.MELTANO_YML: meltano_yml_getter,
            SettingValueSource.DB: db_getter,
            SettingValueSource.DEFAULT: default_getter,
        }

        for source, getter in config_getters.items():
            value = getter()
            if value is not None:
                break

        if setting_def:
            value = self.cast_value(setting_def, value)

            # we don't want to leak secure informations
            # so we redact all `passwords`
            if redacted and value and self.is_kind_redacted(setting_def.kind):
                value = REDACTED_VALUE

        return value, source

    def expand_env_vars(self, raw_value):
        if not isinstance(raw_value, str):
            return raw_value

        # find viable substitutions
        var_matcher = re.compile(
            """
            \$                 # starts with a '$'
            (?:                # either $VAR or ${VAR}
                {(\w+)}|(\w+)  # capture the variable name as group[0] or group[1]
            )
            """,
            re.VERBOSE,
        )

        def subst(match) -> str:
            try:
                # the variable can be in either group
                var = next(var for var in match.groups() if var)
                val = str(self.env[var])

                if not val:
                    logging.warning(f"Variable {var} is empty.")

                return val
            except KeyError as e:
                logging.warning(f"Variable {var} is missing from the environment.")
                return None

        fullmatch = re.fullmatch(var_matcher, raw_value)
        if fullmatch:
            # If the entire value is an env var reference, return None if it isn't set
            return subst(fullmatch)

        return re.sub(var_matcher, subst, raw_value)
