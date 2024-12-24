import json
import pika
from src.core.messaging import get_rabbitmq_connection

def publish_login_user_command(email: str, password: str):
    """
    Publica un comando asíncrono para 'login_user'.
    Si deseas manejar login via RabbitMQ (CQRS),
    en lugar de hacerlo de forma sincrónica.
    """
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='auth_commands', durable=True)

    message = {
        "action": "login_user",
        "email": email,
        "password": password
    }

    channel.basic_publish(
        exchange='',
        routing_key='auth_commands',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
