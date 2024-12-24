
import pika
import uuid
import json
from threading import Lock
from src.core.config import settings


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

