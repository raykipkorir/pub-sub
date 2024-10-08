import redis
from django.conf import settings

from integrations.base import MessageBrokerInterface


class Redis(MessageBrokerInterface):
    """Redis message broker."""

    def __init__(self):
        super().__init__()
        self.host = settings.REDIS_CONFIG["REDIS_HOST"]
        self.port = settings.REDIS_CONFIG["REDIS_PORT"]

        self._client = self._connect()

    def _connect(self):
        """Connect to a Redis instance."""
        client = redis.StrictRedis(host=self.host, port=self.port, db=1)
        return client

    def subscribe(self, channel_name):
        """Subscribe to a channel."""
        from integrations.utilities import create_notification, decode_message

        pub_sub = self._client.pubsub()
        pub_sub.subscribe(channel_name)
        for message in pub_sub.listen():
            if message["type"] == "message":
                if message.get("data"):
                    data = decode_message(message.get("data"))
                    create_notification(data)

    def publish(self, channel_name, json_data):
        """Publish to a channel."""
        self._client.publish(channel_name, json_data)
