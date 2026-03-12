from decimal import Decimal

import pytest

from app.services.price_service import PriceService


class DummyRepository:
    def __init__(self) -> None:
        self.saved = []
        self.history = []
        self.latest = None
        self.by_range = []

    async def add_price(self, ticker, price, timestamp_unix):
        item = {
            "ticker": ticker,
            "price": price,
            "timestamp_unix": timestamp_unix,
        }
        self.saved.append(item)
        return item

    async def get_all_by_ticker(self, ticker):
        return self.history

    async def get_latest_by_ticker(self, ticker):
        return self.latest

    async def get_by_ticker_and_date_range(self, ticker, from_ts, to_ts):
        return self.by_range


class DummySession:
    async def commit(self):
        return None

    async def rollback(self):
        return None


@pytest.mark.asyncio
async def test_save_price_success():
    service = PriceService(DummySession())
    service.repository = DummyRepository()

    result = await service.save_price(
        ticker="btc_usd",
        price=Decimal("70000.12"),
        timestamp_unix=1234567890,
    )

    assert result["ticker"] == "btc_usd"
    assert result["price"] == Decimal("70000.12")
    assert result["timestamp_unix"] == 1234567890


@pytest.mark.asyncio
async def test_save_price_invalid_ticker():
    service = PriceService(DummySession())
    service.repository = DummyRepository()

    with pytest.raises(ValueError):
        await service.save_price(
            ticker="sol_usd",
            price=Decimal("123.45"),
            timestamp_unix=1234567890,
        )


@pytest.mark.asyncio
async def test_get_latest_price():
    service = PriceService(DummySession())
    repository = DummyRepository()
    repository.latest = {
        "ticker": "btc_usd",
        "price": Decimal("70100.00"),
        "timestamp_unix": 1111111111,
    }
    service.repository = repository

    result = await service.get_latest_price("btc_usd")

    assert result["ticker"] == "btc_usd"
    assert result["price"] == Decimal("70100.00")