import os
from typing import Iterator

from sqlalchemy import create_engine
from pandas import DataFrame


class PostgresLoader:
    def __init__(self):
        # we can ask user to enter all this variables in one connection string
        username = os.environ.get("PG_USERNAME")
        password = os.environ.get("PG_PASSWORD")
        host = os.environ.get("PG_ADDRESS")
        port = os.environ.get("PG_PORT")
        db_name = os.environ.get("PG_DATABASE")
        connection_string = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
        self.connection = create_engine(connection_string)

    def load(self, dataframes: {'itemName': str, 'data': Iterator[DataFrame]}):
        # apply_schema()
        # load DF to db
        for df in dataframes:
            df.to_sql(name=schema_name, con=self.connection, index=False)
