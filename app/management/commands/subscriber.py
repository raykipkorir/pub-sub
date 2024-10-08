from django.conf import settings
from django.core.management.base import BaseCommand

from integrations.rabbitmq import RabbitMQ
from integrations.redis import Redis
from integrations.utilities import get_rabbitmq_client, get_redis_client

default_queue = settings.RABBITMQ_CONFIG["QUEUES"]["DEFAULT_QUEUE"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Consumer is running")

        redis_broker: Redis = get_redis_client()
        rabbitmq_broker: RabbitMQ = get_rabbitmq_client()

        # rabbitmq
        rabbitmq_broker.subscribe(default_queue)

        # redis
        redis_broker.subscribe("notification.new")
