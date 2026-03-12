from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Price


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_price(
        self,
        ticker: str,
        price: Decimal,
        timestamp_unix: int,
    ) -> Price:
        price_record = Price(
            ticker=ticker,
            price=price,
            timestamp_unix=timestamp_unix,
        )
        self.session.add(price_record)
        await self.session.flush()
        await self.session.refresh(price_record)
        return price_record

    async def get_all_by_ticker(self, ticker: str) -> Sequence[Price]:
        query: Select[tuple[Price]] = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.timestamp_unix.asc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_latest_by_ticker(self, ticker: str) -> Price | None:
        query: Select[tuple[Price]] = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(desc(Price.timestamp_unix))
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_ticker_and_date_range(
        self,
        ticker: str,
        from_ts: int,
        to_ts: int,
    ) -> Sequence[Price]:
        query: Select[tuple[Price]] = (
            select(Price)
            .where(
                Price.ticker == ticker,
                Price.timestamp_unix >= from_ts,
                Price.timestamp_unix <= to_ts,
            )
            .order_by(Price.timestamp_unix.asc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()