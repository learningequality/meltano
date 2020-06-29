from typing import Iterable, Dict, List

from meltano.core.project_settings_service import ProjectSettingsService
from meltano.core.settings_service import (
    SettingsService,
    SettingMissingError,
    SettingValueSource,
    SettingValueStore,
    REDACTED_VALUE,
)
from meltano.core.plugin import PluginRef, PluginType, Plugin, PluginInstall, Profile
from meltano.core.plugin.error import PluginMissingError


class PluginSettingsService:
    def __init__(self, *args, env_override={}, config_override={}, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.env_override = env_override
        self.config_override = config_override

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

    def build(self, session=None, plugin=None):
        return SpecificPluginSettingsService(
            plugin,
            *self._args,
            **self._kwargs,
            session=session,
            env_override=self.env_override,
            config_override=self.config_override,
        )

    def profile_with_config(self, session, plugin: PluginRef, *args, **kwargs):
        return self.build(session, plugin).profile_with_config(*args, **kwargs)

    def profiles_with_config(self, session, plugin: PluginRef, *args, **kwargs):
        return self.build(session, plugin).profiles_with_config(*args, **kwargs)

    def config_with_sources(self, session, plugin: PluginRef, *args, **kwargs):
        return self.build(session, plugin).config_with_sources(*args, **kwargs)

    @property
    def env(self):
        return self.build().env

    def as_config(self, session, plugin: PluginRef, *args, **kwargs):
        return self.build(session, plugin).as_config(*args, **kwargs)

    def as_env(self, session, plugin: PluginRef, *args, **kwargs):
        return self.build(session, plugin).as_env(*args, **kwargs)

    def set(
        self, session, plugin: PluginRef, *args, store=SettingValueStore.DB, **kwargs
    ):
        return self.build(session, plugin).set(*args, **kwargs, store=store)

    def unset(
        self, session, plugin: PluginRef, *args, store=SettingValueStore.DB, **kwargs
    ):
        return self.build(session, plugin).unset(*args, **kwargs, store=store)

    def reset(
        self, session, plugin: PluginRef, *args, store=SettingValueStore.DB, **kwargs
    ):
        return self.build(session, plugin).reset(*args, **kwargs, store=store)

    def get_value(self, session, plugin: PluginRef, *args, **kwargs):
        return self.build(session, plugin).get_value(*args, **kwargs)

    def find_setting(self, plugin: PluginRef, *args, **kwargs):
        return self.build(plugin=plugin).find_setting(*args, **kwargs)

    def setting_env(self, setting_def, plugin: PluginRef):
        return self.build(plugin=plugin).setting_env(setting_def)


class SpecificPluginSettingsService(SettingsService):
    def __init__(self, plugin: PluginRef, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin = plugin

        self.project_settings_service = ProjectSettingsService(
            self.project, self.session
        )
        self.env_override = {
            **self.project_settings_service.as_env(),
            **self.env_override,
        }

        self.plugin_def = self.discovery_service.find_plugin(
            self.plugin.type, self.plugin.name
        )
        self._plugin_install = None

        self._env_namespace = self.plugin_def.namespace
        self._db_namespace = self.plugin.qualified_name
        self._definitions = self.plugin_def.settings

    @property
    def plugin_install(self):
        if not self._plugin_install:
            self._plugin_install = self.config_service.get_plugin(self.plugin)

        return self._plugin_install

    @property
    def _current_config(self) -> Dict:
        return self.plugin_install.current_config

    def _update_config(self):
        self.config_service.update_plugin(self.plugin_install)

    def profile_with_config(self, profile: Profile, redacted=False):
        self.plugin_install.use_profile(profile)

        full_config = self.config_with_sources(redacted=redacted)

        return {
            **profile.canonical(),
            "config": {key: config["value"] for key, config in full_config.items()},
            "config_sources": {
                key: config["source"] for key, config in full_config.items()
            },
        }

    def profiles_with_config(self, redacted=False) -> List[Dict]:
        return [
            self.profile_with_config(profile, redacted=redacted)
            for profile in (Profile.DEFAULT, *self.plugin_install.profiles)
        ]
