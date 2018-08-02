import asyncio
import datetime
from dateutil.relativedelta import relativedelta
from Extract.common.utils import create_aiohttp_session, fetch

FASTLY_API_SERVER = "https://api.fastly.com/"


def get_endpoint_url(endpoint) -> str:
    """
    helper function that adds the Fastly domain to the Endpoints that are generated in the body of the class
    :return:
    """
    return f'{FASTLY_API_SERVER}{endpoint}'


class FastlyExtractor:
    """
    Extractor for the Fastly Billing API
    """

    def __init__(self):
        self.today = datetime.date.today()
        # This is historical data starts after this period
        self.start_date = datetime.date(2017, 8, 1)

    async def get_entities(self):
        entities = []
        async with create_aiohttp_session() as session:
            date = self.start_date
            while date < self.today:
                billing_endpoint = f'billing/v2/year/{date.year:04}/month/{date.month:02}'
                billing_url = get_endpoint_url(billing_endpoint)
                entity = asyncio.ensure_future(fetch(url=billing_url, session=session))
                entities.append(entity)
                date += relativedelta(months=1)
            return await asyncio.gather(*entities)

    def extract(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.get_entities())
        results = loop.run_until_complete(future)
        return results
