from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PriceResponse(BaseModel):
    id: int
    ticker: str
    price: Decimal
    timestamp_unix: int

    model_config = ConfigDict(from_attributes=True)


class LatestPriceResponse(BaseModel):
    ticker: str
    price: Decimal
    timestamp_unix: int