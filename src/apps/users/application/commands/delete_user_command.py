import json
import pika
from src.core.messaging import get_rabbitmq_connection

def publish_delete_user_command(user_id: int):
    """
    Publishes a command to delete a user account.

    Args:
        user_id (int): The ID of the user to delete.

    Raises:
        ValueError: If the user_id is not valid.
    """
    if not isinstance(user_id, int):
        raise ValueError("Invalid user_id: must be an integer")

    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue="users_commands", durable=True)

    message = {
        "action": "delete_user",
        "user_id": user_id
    }

    channel.basic_publish(
        exchange="",
        routing_key="users_commands",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()