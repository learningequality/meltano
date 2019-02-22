import yaml
import fnmatch
import re
from functools import reduce
from collections import namedtuple
from enum import Enum


class YAMLEnum(str, Enum):
    def __str__(self):
        return self.value

    @staticmethod
    def yaml_representer(dumper, obj):
        return dumper.represent_scalar("tag:yaml.org,2002:str", str(obj))


yaml.add_multi_representer(YAMLEnum, YAMLEnum.yaml_representer)

class IncompatibleELTContext(Exception):
    """
    Occurs when the ELTContext of all invoked plugins cannot
    be merged.
    """
    pass


class ELTContext():
    __attrs__ = ("source_name", "warehouse_type", "transformer")

    def __init__(self,
                 source_name=None,
                 warehouse_type=None,
                 transformer=None):
        self.source_name = source_name
        self.warehouse_type = warehouse_type
        self.transformer = transformer

    @classmethod
    def merge(cls, *contexts):
        merged = ELTContext()

        for ctx in contexts:
            for attr in cls.__attrs__:
                old_value = getattr(merged, attr)
                new_value = getattr(ctx, attr)
                if old_value and new_value and old_value != new_value:
                    print(old_value)
                    print(new_value)
                    raise IncompatibleELTContext()
                else:
                    setattr(merged, attr, new_value)

        return merged

    def __eq__(self, other):
        return (self.source_name == other.source_name
                and self.warehouse_type == other.warehouse_type
                and self.transformer == other.transformer)

    def __repr__(self):
        return f"<ELT from={self.source_name} into={self.warehouse_type} xform={self.transformer}>"


class PluginType(YAMLEnum):
    EXTRACTORS = "extractors"
    LOADERS = "loaders"
    TRANSFORMERS = "transformers"
    TRANSFORMS = "transforms"
    ALL = "all"

    def __str__(self):
        return self.value


class Plugin:
    def __init__(
        self,
        plugin_type: PluginType,
        name: str,
        pip_url=None,
        config=None,
        select=None,
        **extras
    ):
        self.name = name
        self.type = plugin_type
        self.pip_url = pip_url
        self.config = config
        self._select = set(select or [])
        self._extras = extras or {}

    def canonical(self):
        canonical = {
            "name": self.name,
            "pip_url": self.pip_url,
            "config": self.config,
            **self._extras,
        }

        if self._select:
            canonical.update({"select": list(self._select)})

        if self._extras:
            canonical.update(**self._extras)

        return canonical

    @property
    def elt_context(self):
        if not self.__elt_context__:
            raise NotImplemented("__elt_context__ is not set, cannot infer from name.")

        match = re.search(self.__elt_context__, self.name)
        return ELTContext(**match.groupdict())

    @property
    def config_files(self):
        """Return a list of stubbed files created for this plugin."""
        return []

    @property
    def output_files(self):
        return []

    @property
    def select(self):
        return self._select or {"*.*"}

    @select.setter
    def select(self, patterns):
        self._select = set(patterns)

    def add_select_filter(self, filter: str):
        self._select.add(filter)

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type
