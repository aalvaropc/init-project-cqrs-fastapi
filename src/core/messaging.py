import pika
from src.core.config import settings


def get_rabbitmq_connection():
    """
    Establishes a connection to the RabbitMQ server.

    This function creates a connection to RabbitMQ using the credentials
    and connection parameters specified in the application settings.

    Returns:
        pika.BlockingConnection: An established connection to the RabbitMQ server.

    Raises:
        pika.exceptions.AMQPError: If the connection to RabbitMQ fails.
    """
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
    )
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials,
    )
    return pika.BlockingConnection(parameters)
