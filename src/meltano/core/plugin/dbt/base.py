from meltano.core.behavior.hookable import HookObject, hook
from meltano.core.plugin import Plugin, PluginType, ELTContext


class DbtPlugin(Plugin, HookObject):
    __plugin_type__ = PluginType.TRANSFORMERS
    __elt_context__ = r"(?P<transformer>.*)"

    def __init__(self, *args, **kwargs):
        super().__init__(self.__class__.__plugin_type__, *args, **kwargs)


class DbtTransformPlugin(Plugin, HookObject):
    __plugin_type__ = PluginType.TRANSFORMS
    __elt_context__ = r"(?P<transformer>.*?)-(?P<source_name>.*)-(?P<warehouse_type>.*)"

    def __init__(self, *args, **kwargs):
        super().__init__(self.__class__.__plugin_type__, *args, **kwargs)
