import json
import pika
from src.core.messaging import get_rabbitmq_connection

def publish_update_user_command(user_id: int, name: str, email: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='users_commands', durable=True)

    message = {
        "action": "update_user",
        "user_id": user_id,
        "name": name,
        "email": email
    }

    channel.basic_publish(
        exchange='',
        routing_key='users_commands',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()


# import json
# import pika
# from src.core.messaging import get_rabbitmq_connection


# def publish_update_user_command(user_id: int, name: str = None, email: str = None):
#     """
#     Publishes a command to RabbitMQ to update a user's profile.

#     Args:
#         user_id (int): The ID of the user to update.
#         name (str): The new name for the user (optional).
#         email (str): The new email for the user (optional).
#     """
#     connection = get_rabbitmq_connection()
#     channel = connection.channel()
#     channel.queue_declare(queue='users_commands', durable=True)

#     message = {
#         "action": "update_user",
#         "user_id": user_id,
#         "name": name,
#         "email": email
#     }

#     channel.basic_publish(
#         exchange='',
#         routing_key='users_commands',
#         body=json.dumps(message),
#         properties=pika.BasicProperties(delivery_mode=2)
#     )
#     connection.close()
