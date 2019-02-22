from typing import Dict

from .base import Plugin, PluginType, ELTContext
from .singer import SingerTap, SingerTarget
from .dbt import DbtPlugin, DbtTransformPlugin


def infer_plugin_name(plugin_type: PluginType, elt_context: ELTContext):
    strategy = {
        PluginType.EXTRACTORS: lambda: f"tap-{elt_context.source_name}",
        PluginType.LOADERS: lambda: f"target-{elt_context.warehouse_type}",
        PluginType.TRANSFORMERS: lambda: elt_context.transformer,
        PluginType.TRANSFORMS: lambda: f"{elt_context.transformer}-{elt_context.source_name}-{elt_context.warehouse_type}",
    }

    return strategy[plugin_type]()


def plugin_class(plugin_type: PluginType):
    class_map = {
        PluginType.EXTRACTORS: SingerTap,
        PluginType.LOADERS: SingerTarget,
        PluginType.TRANSFORMERS: DbtPlugin,
        PluginType.TRANSFORMS: DbtTransformPlugin,
    }

    return class_map[plugin_type]


def plugin_factory(plugin_type: PluginType, plugin_def: Dict):
    # this will parse the discovery file and create an instance of the
    # corresponding `plugin_class` for all the plugins.
    return plugin_class(plugin_type)(**plugin_def)
