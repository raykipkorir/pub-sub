import json
from datetime import datetime

from django.conf import settings
from django.http.response import HttpResponse

from app.models import Notification
from integrations.rabbitmq import RabbitMQ
from integrations.redis import Redis
from integrations.utilities import get_rabbitmq_client, get_redis_client


def index(request):
    notifications = Notification.objects.all()
    data = []
    for notification in notifications:
        data.append(str(notification) + " // ")

    if data:
        return HttpResponse(data)
    else:
        return HttpResponse("No new notifications.")


def publish(request):
    lst = str(datetime.now()).split(".")
    date_time = lst[0]
    data = {
        "title": "Welcome",
        "message": "Hello to all connected clients",
        "date": date_time,
    }
    json_data = json.dumps(data)

    # rabbitmq
    broker = get_rabbitmq_client()
    exchanges = settings.RABBITMQ_CONFIG["EXCHANGES"]
    broker.publish(exchanges["DEFAULT_EXCHANGE"], "notification.new", json_data)

    # redis
    redis_broker = get_redis_client()
    redis_broker.publish("notification.new", json_data)

    return HttpResponse("New notification has been published.")
