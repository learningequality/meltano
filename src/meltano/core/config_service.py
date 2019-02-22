import os
import yaml
from typing import Dict, List, Optional

from .project import Project
from .plugin import Plugin, PluginType
from .plugin.singer import SingerTap, SingerTarget
from .plugin.dbt import DbtPlugin, DbtTransformPlugin
from .plugin.error import PluginMissingError


def infer_plugin_name(self, plugin_type: PluginType, elt_context: ELTContext):
    strategy = {
        PluginType.EXTRACTORS: lambda: f"tap-{elt_context.source_name}",
        PluginType.LOADERS: lambda: f"target-{elt_context.warehouse_type}",
        PluginType.TRANSFORMERS: lambda: elt_context.transformer,
        PluginType.TRANSFORMS: lambda: f"{elt_context.transfomer}-{elt_context.source_name}-{elt_context.warehouse_type}",
    }

    return plugin_class[plugin_type].infer(elt_context)


def plugin_class(self, plugin_type: PluginType):
    class_map = {
        PluginType.EXTRACTORS: SingerTap,
        PluginType.LOADERS: SingerTarget,
        PluginType.TRANSFORMERS: DbtPlugin,
        PluginType.TRANSFORMS: DbtTransformPlugin,
    }

    return class_map[plugin_type]


def plugin_factory(self, plugin_type: PluginType, plugin_def: Dict):
    plugin_class = plugin_class[plugin_type]

    # this will parse the discovery file and create an instance of the
    # corresponding `plugin_class` for all the plugins.
    return plugin_class[plugin_type](**plugin_def)


class ConfigService:
    def __init__(self, project: Project):
        self.project = project

    def make_meltano_secret_dir(self):
        os.makedirs(self.project.meltano_dir(), exist_ok=True)

    def get_plugin(self, plugin_type: PluginType, plugin_name: str):
        try:
            return next(
                plugin
                for plugin in self.plugins()
                if plugin.type == plugin_type and plugin.name == plugin_name
            )
        except StopIteration:
            raise PluginMissingError(plugin_name)

    def get_extractors(self):
        return filter(lambda p: p.type == PluginType.EXTRACTORS, self.plugins())

    def get_loaders(self):
        return filter(lambda p: p.type == PluginType.LOADERS, self.plugins())

    def get_transformers(self):
        return filter(lambda p: p.type == PluginType.TRANSFORMERS, self.plugins())

    def get_transforms(self):
        return filter(lambda p: p.type == PluginType.TRANSFORMS, self.plugins())

    def get_database(self, database_name):
        return yaml.load(
            open(self.project.meltano_dir(f".database_{database_name}.yml"))
        )

    def plugins(self) -> List[Plugin]:
        """Parse the meltano.yml file and return it as `Plugin` instances."""
        # this will parse the meltano.yml file and create an instance of the
        # corresponding `plugin_class` for all the plugins.
        return (
            self.plugin_generator(plugin_type, plugin_def)
            for plugin_type, plugin_defs in self.project.meltano.get(
                "plugins", {}
            ).items()
            for plugin_def in plugin_defs
        )
