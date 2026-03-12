from decimal import Decimal
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.db.session import get_db_session
from app.main import app
from app.services.price_service import PriceService


class DummySession:
    pass


async def override_get_db_session():
    yield DummySession()


app.dependency_overrides[get_db_session] = override_get_db_session


def test_get_latest_price(monkeypatch):
    async def mock_get_latest_price(self, ticker: str):
        return SimpleNamespace(
            ticker=ticker,
            price=Decimal("70100.55"),
            timestamp_unix=1234567890,
        )

    monkeypatch.setattr(PriceService, "get_latest_price", mock_get_latest_price)

    client = TestClient(app)
    response = client.get("/prices/latest", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "btc_usd"
    assert data["price"] == "70100.55"
    assert data["timestamp_unix"] == 1234567890


def test_get_latest_price_not_found(monkeypatch):
    async def mock_get_latest_price(self, ticker: str):
        return None

    monkeypatch.setattr(PriceService, "get_latest_price", mock_get_latest_price)

    client = TestClient(app)
    response = client.get("/prices/latest", params={"ticker": "btc_usd"})

    assert response.status_code == 404


def test_get_prices_by_date_range_invalid_range():
    client = TestClient(app)
    response = client.get(
        "/prices/by-date",
        params={
            "ticker": "btc_usd",
            "from_ts": 200,
            "to_ts": 100,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "from_ts must be less than or equal to to_ts"