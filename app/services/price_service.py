from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Price
from app.repositories.price_repository import PriceRepository


SUPPORTED_TICKERS = {"btc_usd", "eth_usd"}


class PriceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = PriceRepository(session)

    @staticmethod
    def validate_ticker(ticker: str) -> None:
        if ticker not in SUPPORTED_TICKERS:
            raise ValueError(
                f"Unsupported ticker '{ticker}'. Supported tickers: {', '.join(sorted(SUPPORTED_TICKERS))}"
            )

    async def save_price(
        self,
        ticker: str,
        price: Decimal,
        timestamp_unix: int,
    ) -> Price:
        self.validate_ticker(ticker)
        return await self.repository.add_price(
            ticker=ticker,
            price=price,
            timestamp_unix=timestamp_unix,
        )

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def get_price_history(self, ticker: str) -> Sequence[Price]:
        self.validate_ticker(ticker)
        return await self.repository.get_all_by_ticker(ticker)

    async def get_latest_price(self, ticker: str) -> Price | None:
        self.validate_ticker(ticker)
        return await self.repository.get_latest_by_ticker(ticker)

    async def get_prices_by_date_range(
        self,
        ticker: str,
        from_ts: int,
        to_ts: int,
    ) -> Sequence[Price]:
        self.validate_ticker(ticker)
        return await self.repository.get_by_ticker_and_date_range(
            ticker=ticker,
            from_ts=from_ts,
            to_ts=to_ts,
        )