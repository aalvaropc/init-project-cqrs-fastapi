import jwt
from src.core.config import settings
import json
import pika
from sqlalchemy.orm import Session
from src.core.db import SessionLocalWriter
from src.apps.users.domain.use_cases import (
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)
from src.apps.users.infrastructure.sqlalchemy_repositories_writer import UserRepositoryWriter
import logging
import sys


# Configuración de logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("user_consumer")

# Constantes
RABBITMQ_HOST = "rabbitmq"
USERS_COMMANDS_QUEUE = "users_commands"


def handle_create_user(repo, data):
    """
    Procesa el comando `create_user`.
    """
    logger.info("Processing create_user action")
    use_case = CreateUserUseCase(repo)
    use_case.execute(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )


def handle_update_user(repo, data):
    """
    Procesa el comando `update_user`.
    """
    logger.info("Processing update_user action")

    token = data["user_id"]  # JWT token
    name = data.get("name")
    email = data.get("email")

    try:
        # Extrae el user_id desde el token
        user_id = extract_user_id_from_token(token)

        # Llama al repositorio para actualizar el usuario
        updated_user = repo.update_user(user_id=user_id, name=name, email=email)
        if not updated_user:
            logger.warning(f"User with ID {user_id} not found.")
    except ValueError as e:
        logger.error(f"Token error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise



def handle_delete_user(repo, data):
    """
    Processes the `delete_user` command.

    Args:
        repo (UserRepositoryWriter): Repository instance.
        data (dict): Command data containing the user ID.

    Raises:
        ValueError: If the user ID is not valid.
    Exception: If the deletion process fails.
    """
    logger.info("Processing delete_user action")
    token = data.get("user_id")

    if not token:
        raise ValueError("Missing token for delete_user action")

    try:
        user_id = extract_user_id_from_token(token)
        use_case = DeleteUserUseCase(repo)
        use_case.execute(user_id=user_id)
    except ValueError as e:
        logger.error(f"Token error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise


def callback(ch, method, properties, body):
    """
    RabbitMQ callback to process messages from the `users_commands` queue.

    Args:
        ch (pika.channel.Channel): The channel instance.
        method (pika.spec.Basic.Deliver): Delivery method.
        properties (pika.spec.BasicProperties): Message properties.
        body (bytes): The message body.

    Raises:
        Exception: For unhandled errors during message processing.
    """
    logger.info(f"[USERS] Received message: {body}")
    data = json.loads(body)
    action = data.get("action")
    db: Session = SessionLocalWriter()

    try:
        repo = UserRepositoryWriter(db)

        if action == "create_user":
            handle_create_user(repo, data)
        elif action == "update_user":
            handle_update_user(repo, data)
        elif action == "delete_user":
            handle_delete_user(repo, data)
        else:
            logger.warning(f"Unknown action: {action}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        db.commit()
        logger.info(f"[USERS] Successfully processed action: {action}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as ex:
        logger.error(f"[USERS] Error processing message: {ex}")
        db.rollback()
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        db.close()


def user_commands_consumer():
    """
    Initializes the RabbitMQ consumer for the `users_commands` queue.

    Raises:
        SystemExit: If the consumer fails to initialize.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=USERS_COMMANDS_QUEUE, durable=True)
        logger.info(f"[USERS] Connected to RabbitMQ and declared queue '{USERS_COMMANDS_QUEUE}'.")

        channel.basic_consume(queue=USERS_COMMANDS_QUEUE, on_message_callback=callback)
        logger.info("[USERS] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"[USERS] Error initializing consumer: {e}")
        sys.exit(1)

def extract_user_id_from_token(token: str) -> int:
    """
    Extracts the user ID from a JWT.

    Args:
        token (str): JWT token.

    Returns:
        int: User ID extracted from the token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired.")
        raise ValueError("Token expired.")
    except jwt.InvalidTokenError:
        logger.error("Invalid token.")
        raise ValueError("Invalid token.")
    
if __name__ == "__main__":
    user_commands_consumer()
