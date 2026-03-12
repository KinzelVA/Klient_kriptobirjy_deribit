from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "deribit_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.fetch_prices"],
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

celery_app.conf.beat_schedule = {
    "fetch-deribit-prices-every-minute": {
        "task": "app.tasks.fetch_prices.fetch_and_store_prices",
        "schedule": 60.0,
    }
}