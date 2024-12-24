# import json
# import pika
# from sqlalchemy.orm import Session

# from src.core.config import settings
# from src.core.db import SessionLocalWriter
# from src.apps.auth.domain.use_cases import LoginUserUseCase
# from src.apps.auth.infrastructure.auth_repository import AuthRepository
# from src.apps.auth.infrastructure.jwt_service import JWTService
# from src.apps.auth.domain.exceptions import (
#     AuthenticationError,
#     TokenBlacklistError
# )

# import logging
# import sys

# logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# logger = logging.getLogger("auth_consumer")

# def auth_commands_consumer():
#     """
#     Consumer para la cola 'auth_commands'.
#     Maneja login y sign out de usuarios de forma asíncrona.
#     Responde con el JWT al cliente.
#     """
#     try:

#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(
#                 host=settings.RABBITMQ_HOST,
#                 port=settings.RABBITMQ_PORT,
#                 credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
#             )
#         )
#         channel = connection.channel()
#         channel.queue_declare(queue='auth_commands', durable=True)
#         logger.info("[AUTH] Connected to RabbitMQ and declared queue 'auth_commands'.")

#         def callback(ch, method, properties, body):
#             logger.info(f"[AUTH] Received message: {body}")
#             data = json.loads(body)
#             action = data.get("action")
#             if not action:
#                 logger.error("[AUTH] Missing action in message.")
#                 ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
#                 return

#             db: Session = SessionLocalWriter()
#             jwt_service = JWTService(
#                 secret_key=settings.JWT_SECRET,
#                 algorithm=settings.JWT_ALGORITHM,
#                 expire_minutes=settings.JWT_EXPIRE_MINUTES
#             )
#             repo = AuthRepository(db)

#             try:
#                 if action == "login_user":
#                     logger.info("[AUTH] Processing login_user action")
#                     email = data.get("email")
#                     password = data.get("password")

#                     if not email or not password:
#                         raise AuthenticationError("Email y contraseña son obligatorios.")

#                     use_case = LoginUserUseCase(repo, jwt_service)
#                     access_token = use_case.execute(email=email, password=password)
#                     response = {"access_token": access_token, "token_type": "bearer"}

#                 elif action == "sign_out":
#                     logger.info("[AUTH] Processing sign_out action")
#                     token = data.get("token")
#                     if not token:
#                         raise TokenBlacklistError("Token no proporcionado para sign out.")
#                     repo.blacklist_token(token)
#                     response = {"detail": "Successfully signed out."}

#                 else:
#                     logger.warning(f"[AUTH] Unknown action: {action}")
#                     response = {"detail": f"Unknown action: {action}"}

#                 db.commit()
#                 logger.info(f"[AUTH] Successfully processed action: {action}")

#                 if properties.reply_to:
#                     channel.basic_publish(
#                         exchange='',
#                         routing_key=properties.reply_to,
#                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
#                         body=json.dumps(response)
#                     )
#                 ch.basic_ack(delivery_tag=method.delivery_tag)

#             except (AuthenticationError, TokenBlacklistError) as ex:
#                 logger.error(f"[AUTH] Authentication-related error: {ex}")
#                 db.rollback()
#                 response = {"detail": str(ex)}
#                 if properties.reply_to:
#                     channel.basic_publish(
#                         exchange='',
#                         routing_key=properties.reply_to,
#                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
#                         body=json.dumps(response)
#                     )
#                 ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

#             except Exception as ex:
#                 logger.error(f"[AUTH] General error processing message: {ex}")
#                 db.rollback()
#                 response = {"detail": "Internal server error."}
#                 if properties.reply_to:
#                     channel.basic_publish(
#                         exchange='',
#                         routing_key=properties.reply_to,
#                         properties=pika.BasicProperties(correlation_id=properties.correlation_id),
#                         body=json.dumps(response)
#                     )
#                 ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

#             finally:
#                 db.close()

#         channel.basic_consume(queue='auth_commands', on_message_callback=callback)
#         logger.info("[AUTH] Waiting for messages")
#         channel.start_consuming()

#     except Exception as e:
#         logger.error(f"[AUTH] Error initializing consumer: {e}")
#         sys.exit(1)


# if __name__ == "__main__":
#     auth_commands_consumer()



import json
import pika
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.db import SessionLocalWriter
from src.apps.auth.domain.use_cases import LoginUserUseCase
from src.apps.auth.infrastructure.auth_repository import AuthRepository
from src.core.messaging import create_rabbitmq_connection
from src.apps.auth.infrastructure.jwt_service import JWTService
from src.apps.auth.domain.exceptions import (
    AuthenticationError,
    TokenBlacklistError,
)
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("auth_consumer")


# def create_rabbitmq_connection():
#     """
#     Creates a RabbitMQ connection using the provided settings.

#     Returns:
#         pika.BlockingConnection: A blocking connection to RabbitMQ.
#     """
#     return pika.BlockingConnection(
#         pika.ConnectionParameters(
#             host=settings.RABBITMQ_HOST,
#             port=settings.RABBITMQ_PORT,
#             credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD),
#         )
#     )


def handle_login_user(data, repo, jwt_service):
    """
    Handles the login_user action by validating credentials and generating a JWT.

    Args:
        data (dict): The message data containing email and password.
        repo (AuthRepository): The repository for authentication operations.
        jwt_service (JWTService): Service for handling JWT generation and validation.

    Returns:
        dict: A dictionary containing the generated access token.
    """
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise AuthenticationError("Email and password are required.")

    use_case = LoginUserUseCase(repo, jwt_service)
    access_token = use_case.execute(email=email, password=password)
    return {"access_token": access_token, "token_type": "bearer"}


def handle_sign_out(data, repo):
    """
    Handles the sign_out action by blacklisting the provided token.

    Args:
        data (dict): The message data containing the token to blacklist.
        repo (AuthRepository): The repository for authentication operations.

    Returns:
        dict: A dictionary containing a confirmation message.
    """
    token = data.get("token")
    if not token:
        raise TokenBlacklistError("Token not provided for sign out.")

    repo.blacklist_token(token)
    return {"detail": "Successfully signed out."}


def process_message(ch, method, properties, body):
    """
    Processes a message from the auth_commands queue.

    Args:
        ch: The channel object.
        method: The delivery method.
        properties: The message properties.
        body: The message body.
    """
    logger.info(f"[AUTH] Received message: {body}")
    data = json.loads(body)
    action = data.get("action")
    if not action:
        logger.error("[AUTH] Missing action in message.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    db: Session = SessionLocalWriter()
    jwt_service = JWTService(
        secret_key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        expire_minutes=settings.JWT_EXPIRE_MINUTES,
    )
    repo = AuthRepository(db)

    try:
        if action == "login_user":
            logger.info("[AUTH] Processing login_user action")
            response = handle_login_user(data, repo, jwt_service)
        elif action == "sign_out":
            logger.info("[AUTH] Processing sign_out action")
            response = handle_sign_out(data, repo)
        else:
            logger.warning(f"[AUTH] Unknown action: {action}")
            response = {"detail": f"Unknown action: {action}"}

        db.commit()
        logger.info(f"[AUTH] Successfully processed action: {action}")

        if properties.reply_to:
            ch.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response),
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (AuthenticationError, TokenBlacklistError) as ex:
        logger.error(f"[AUTH] Authentication-related error: {ex}")
        db.rollback()
        response = {"detail": str(ex)}
        if properties.reply_to:
            ch.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response),
            )
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as ex:
        logger.error(f"[AUTH] General error processing message: {ex}")
        db.rollback()
        response = {"detail": "Internal server error."}
        if properties.reply_to:
            ch.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response),
            )
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    finally:
        db.close()


def auth_commands_consumer():
    """
    Consumer for the 'auth_commands' queue.

    Listens to messages from RabbitMQ and processes login and sign out actions asynchronously.
    """
    try:
        connection = create_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue="auth_commands", durable=True)
        logger.info("[AUTH] Connected to RabbitMQ and declared queue 'auth_commands'.")

        channel.basic_consume(queue="auth_commands", on_message_callback=process_message)
        logger.info("[AUTH] Waiting for messages")
        channel.start_consuming()

    except Exception as e:
        logger.error(f"[AUTH] Error initializing consumer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    auth_commands_consumer()
