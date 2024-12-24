import json
import pika
from src.core.messaging import get_rabbitmq_connection

def publish_create_user_command(name: str, email: str, password: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='users_commands', durable=True)

    message = {
        "action": "create_user",
        "name": name,
        "email": email,
        "password": password
    }

    channel.basic_publish(
        exchange='',
        routing_key='users_commands',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
