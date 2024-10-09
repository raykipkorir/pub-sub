import pika
from django.conf import settings

from integrations.base import MessageBrokerInterface

default_exchange = settings.RABBITMQ_CONFIG["EXCHANGES"]["DEFAULT_EXCHANGE"]
default_queue = settings.RABBITMQ_CONFIG["QUEUES"]["DEFAULT_QUEUE"]


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
        self.channel.exchange_declare(default_exchange, exchange_type="direct")
        # setup queues
        self.channel.queue_declare(default_queue)
        # bind queues to an exchange
        self.channel.queue_bind(
            default_queue,
            exchange=default_exchange,
            routing_key="notification.new",
        )

    def subscribe(self, queue_name):
        """Subscribe to a queue."""
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self._consume, auto_ack=True
        )
        self.channel.start_consuming()

    def _consume(self, ch, method, properties, body):
        from integrations.utilities import create_notification, decode_message

        data = decode_message(body)
        # define your handlers
        create_notification(data)

    def publish(self, exchange, routing_key, json_data):
        """Publish to an exchange."""
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
