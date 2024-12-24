import json
import pika
from src.core.messaging import get_rabbitmq_connection


def publish_login_user_command(email: str, password: str):
    """
    Publishes an asynchronous command for 'login_user'.
    
    This function is used to handle the login process via RabbitMQ (CQRS),
    instead of performing the operation synchronously.
    
    Args:
        email (str): The email address of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        None
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
