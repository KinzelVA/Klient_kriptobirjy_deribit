import asyncio
import time

from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService


TICKERS_TO_FETCH = ("btc_usd", "eth_usd")


async def _fetch_and_store_prices() -> str:
    current_timestamp = int(time.time())
    client = DeribitClient()

    async with AsyncSessionLocal() as session:
        service = PriceService(session)

        try:
            for ticker in TICKERS_TO_FETCH:
                price = await client.get_index_price(ticker=ticker)
                await service.save_price(
                    ticker=ticker,
                    price=price,
                    timestamp_unix=current_timestamp,
                )

            await service.commit()
            return "ok"
        except Exception:
            await service.rollback()
            raise


@celery_app.task(name="app.tasks.fetch_prices.fetch_and_store_prices")
def fetch_and_store_prices() -> str:
    return asyncio.run(_fetch_and_store_prices())