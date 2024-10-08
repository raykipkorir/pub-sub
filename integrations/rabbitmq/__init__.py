import pika
from django.conf import settings

from integrations.base import MessageBrokerInterface


class RabbitMQ(MessageBrokerInterface):
    """RabbitMQ message broker."""

    def __init__(self):
        super().__init__()
        config: dict = settings.RABBITMQ_CONFIG
        self.host = config["RABBITMQ_HOST"]
        self.port = config["RABBITMQ_PORT"]
        self.user = config["RABBITMQ_USER"]
        self.password = config["RABBITMQ_PASSWORD"]
        self.connection = None
        self.channel = None

        self._connect()

    def _connect(self):
        """Connect to a rabbitmq instance."""
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        # setup exchange - (direct, topic, fanout)
        self.channel.exchange_declare(
            "pub_sub_poc_direct_exchange", exchange_type="direct"
        )
        # setup queues
        self.channel.queue_declare("queue_for_consumer_one")
        # bind queues to an exchange
        self.channel.queue_bind(
            "queue_for_consumer_one",
            exchange="pub_sub_poc_direct_exchange",
            routing_key="notification.new",
        )

    def subscribe(self, queue_name):
        """Subscribe to a channel."""
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.consume, auto_ack=True
        )
        self.channel.start_consuming()

    def consume(self, ch, method, properties, body):
        from integrations.utilities import create_notification, decode_message

        data = decode_message(body)
        create_notification(data)

    def publish(self, exchange, routing_key, json_data):
        """Publish to a channel."""
        if not self.channel:
            raise Exception("Connection is not established.")
        # self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json_data,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
