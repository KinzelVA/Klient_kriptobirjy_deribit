from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.price import LatestPriceResponse, PriceResponse
from app.services.price_service import PriceService


router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/history", response_model=list[PriceResponse])
async def get_price_history(
    ticker: str = Query(..., description="Ticker name, e.g. btc_usd or eth_usd"),
    session: AsyncSession = Depends(get_db_session),
) -> Sequence[PriceResponse]:
    service = PriceService(session)

    try:
        prices = await service.get_price_history(ticker=ticker)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return [PriceResponse.model_validate(price) for price in prices]


@router.get("/latest", response_model=LatestPriceResponse)
async def get_latest_price(
    ticker: str = Query(..., description="Ticker name, e.g. btc_usd or eth_usd"),
    session: AsyncSession = Depends(get_db_session),
) -> LatestPriceResponse:
    service = PriceService(session)

    try:
        price = await service.get_latest_price(ticker=ticker)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if price is None:
        raise HTTPException(status_code=404, detail=f"No data found for ticker '{ticker}'")

    return LatestPriceResponse(
        ticker=price.ticker,
        price=price.price,
        timestamp_unix=price.timestamp_unix,
    )


@router.get("/by-date", response_model=list[PriceResponse])
async def get_prices_by_date_range(
    ticker: str = Query(..., description="Ticker name, e.g. btc_usd or eth_usd"),
    from_ts: int = Query(..., description="Start of Unix timestamp range"),
    to_ts: int = Query(..., description="End of Unix timestamp range"),
    session: AsyncSession = Depends(get_db_session),
) -> Sequence[PriceResponse]:
    if from_ts > to_ts:
        raise HTTPException(status_code=400, detail="from_ts must be less than or equal to to_ts")

    service = PriceService(session)

    try:
        prices = await service.get_prices_by_date_range(
            ticker=ticker,
            from_ts=from_ts,
            to_ts=to_ts,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return [PriceResponse.model_validate(price) for price in prices]