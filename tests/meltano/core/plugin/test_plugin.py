import pytest

from meltano.core.plugin import Plugin, PluginType, ELTContext

@pytest.fixture
def extractor(config_service):
    return config_service.plugin_generator(PluginType.EXTRACTORS, {
        "name": "tap-test-another",
    })


@pytest.fixture
def loader(config_service):
    return config_service.plugin_generator(PluginType.LOADERS, {
        "name": "target-databasist",
    })


@pytest.fixture
def transform(config_service):
    return config_service.plugin_generator(PluginType.TRANSFORMS, {
        "name": "dbt-bigdataset-sqlite",
    })


def test_plugin_elt_context(extractor, loader, transform):
    assert extractor.elt_context == ELTContext(source_name="test-another")
    assert loader.elt_context == ELTContext(warehouse_type="databasist")
    assert transform.elt_context == ELTContext(source_name="bigdataset",
                                               warehouse_type="sqlite",
                                               transformer="dbt")


def test_plugin_elt_context_merge(extractor, loader, transform):
    extractor.name = "tap-source"
    transform.name = "dbt-source-databasist"

    merged = ELTContext.merge(
        extractor.elt_context,
        loader.elt_context,
        transform.elt_context
    )

    assert merged == ELTContext(source_name="source",
                                warehouse_type="databasist",
                                transformer="dbt")
