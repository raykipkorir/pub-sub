import json
import logging

from app.models import Notification
from integrations.rabbitmq import RabbitMQ
from integrations.redis import Redis

LOGGER = logging.getLogger(__name__)


def get_redis_client() -> Redis:
    """Get redis client."""
    broker = Redis()
    return broker


def get_rabbitmq_client() -> RabbitMQ:
    """Get RabbitMQ client."""
    broker = RabbitMQ()
    return broker


def decode_message(message) -> dict:
    json_data = message.decode("utf-8")
    data = json.loads(json_data)
    print(f"Received: {data}")

    return data


def create_notification(data):
    try:
        Notification.objects.create(
            title=data["title"],
            message=data["message"],
            date=data["date"],
        )
    except Exception as err:
        LOGGER.error("Error creating Notification: ", err)
