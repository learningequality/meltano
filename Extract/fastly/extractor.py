import asyncio
import itertools
import logging
import os
import ssl
from typing import Coroutine

import aiohttp
import certifi
from pandas.io.json import json_normalize

FASTLY_API_SERVER = "https://api.fastly.com/"


def get_endpoint_url(endpoint):
    return f'{FASTLY_API_SERVER}{endpoint}'


def create_aiohttp_session():
    headers = {
        'Fastly-Key': os.getenv("FASTLY_API_TOKEN"),
        'Accept': "application/json"
    }
    # SSL stuff is needed to fix errors when requesting https services
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl_context=ssl_context)
    session = aiohttp.ClientSession(headers=headers, connector=connector)
    return session


async def fetch(endpoint, session):
    request_url = get_endpoint_url(endpoint)
    async with session.get(request_url) as response:
        if response.status != 200:
            logging.error(f'[{response.status}] {response.reason} {request_url}')
        return json_normalize(await response.json())


class FastlyExtractor:
    """
    Extractor for the Fastly Billing API
    """

    # async def entities(self):
    #     """
    #     Generates a list of Entity object for entity extract loop to consume
    #     """
    #     async with create_aiohttp_session() as session:
    #         billing = await fetch(endpoint="billing/v2/year/2018/month/06", session=session)
    #         yield self.df_to_entity("Billing", billing)
    async def entities(self):
        async with create_aiohttp_session() as session:
            for year, month in itertools.product(range(2017, 2018), range(1, 12)):
                billing_endpoint = f'billing/v2/year/{year:04}/month/{month:02}'
                try:
                    print(await fetch(endpoint=billing_endpoint, session=session))
                except Exception as err:
                    print(err)

    def extract(self):
        loop = asyncio.get_event_loop()
        entities = loop.run_until_complete(
            self.entities()
        )
        return entities

    def load(self):
        pass

    def transform(self):
        return 'transformed data'

    def run(self):
        result = self.extract()
        transformed = self.transform(result)
        self.load(transformed)
        pass
