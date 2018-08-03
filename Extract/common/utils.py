import logging
import os
import ssl
import aiohttp
import certifi
from pandas.io.json import json_normalize


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


async def fetch(url, session) -> aiohttp.ClientResponse:
    async with session.get(url) as response:
        if response.status != 200:
            logging.error(f'[{response.status}] {response.reason} {url}')
        return await response.json()
