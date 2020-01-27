import pytest

from unittest.mock import patch

from meltano.core.permissions.utils.snowflake_connector import SnowflakeConnector

@pytest.fixture(scope="class")
def test_schemas():
    schemas = [
        "test_db.test_schema1",
        "test_db.test_schema2",
        "test_db.test_schema3",
        "test_db.test_schema4",
        "test_db.test2_schema1",
        "test_db.test2_schema2",
        "test_db.test2_schema3",
        "test_db.test2_schema4",
    ]

    return schemas


class TestSnowflakeConnector:
    def test_snowflaky(self):

        db1 = "analytics.schema.table"
        db2 = "1234raw.schema.table"
        db3 = '"123-with-quotes".schema.table'
        db4 = "1_db-9-RANDOM.schema.table"

        assert SnowflakeConnector.snowflaky(db1) == "analytics.schema.table"
        assert SnowflakeConnector.snowflaky(db2) == "1234raw.schema.table"
        assert SnowflakeConnector.snowflaky(db3) == '"123-with-quotes".schema.table'
        assert SnowflakeConnector.snowflaky(db4) == '"1_db-9-RANDOM".schema.table'

    def test_mocked_schemas(self, test_schemas):

        with patch.object(
            SnowflakeConnector, "show_schemas", return_value=test_schemas
        ), patch.object(
            SnowflakeConnector, "__init__", return_value=None
        ):
            conn = SnowflakeConnector()

            test_schema = 'test_db.test_*'
            schemas = conn.full_schema_list(test_schema)

            assert len(schemas) == 4
