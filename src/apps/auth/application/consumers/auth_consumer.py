import json
import pika
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.db import SessionLocalWriter
from src.apps.auth.domain.use_cases import LoginUserUseCase
from src.apps.auth.infrastructure.auth_repository import AuthRepository
from src.apps.auth.infrastructure.jwt_service import JWTService
from src.apps.auth.domain.exceptions import (
    AuthenticationError,
    AuthorizationError,
    UserNotFoundError,
    InvalidTokenError,
    TokenBlacklistError
)

import logging
import sys

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("auth_consumer")

def auth_commands_consumer():
    """
    Consumer para la cola 'auth_commands'.
    Maneja login y sign out de usuarios de forma asíncrona.
    Responde con el JWT al cliente.
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='auth_commands', durable=True)
        logger.info("[AUTH] Connected to RabbitMQ and declared queue 'auth_commands'.")

        def callback(ch, method, properties, body):
            logger.info(f"[AUTH] Received message: {body}")
            data = json.loads(body)
            action = data.get("action")

            if properties.reply_to:
                # Es una solicitud de RPC
                reply_to = properties.reply_to
                correlation_id = properties.correlation_id
            else:
                reply_to = None

            db: Session = SessionLocalWriter()

            try:
                repo = AuthRepository(db)
                jwt_service = JWTService(
                    secret_key=settings.JWT_SECRET,
                    algorithm=settings.JWT_ALGORITHM,
                    expire_minutes=settings.JWT_EXPIRE_MINUTES
                )

                if action == "login_user":
                    logger.info("Processing login_user action")
                    email = data.get("email")
                    password = data.get("password")
                    use_case = LoginUserUseCase(repo, jwt_service)
                    access_token = use_case.execute(email=email, password=password)
                    response = {"access_token": access_token}
                elif action == "sign_out":
                    logger.info("Processing sign_out action")
                    token = data.get("token")
                    if not token:
                        raise TokenBlacklistError("Token no proporcionado para sign out.")
                    repo.blacklist_token(token)
                    response = {"detail": "Successfully signed out."}
                else:
                    response = {"detail": "Unknown action"}

                db.commit()

                if reply_to:
                    channel.basic_publish(
                        exchange='',
                        routing_key=reply_to,
                        properties=pika.BasicProperties(correlation_id=correlation_id),
                        body=json.dumps(response)
                    )

                logger.info(f"[AUTH] Successfully processed action: {action}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except (AuthenticationError, UserNotFoundError, TokenBlacklistError) as ex:
                logger.error(f"[AUTH] Authentication-related error: {ex}")
                db.rollback()
                if reply_to:
                    response = {"detail": str(ex)}
                    channel.basic_publish(
                        exchange='',
                        routing_key=reply_to,
                        properties=pika.BasicProperties(correlation_id=correlation_id),
                        body=json.dumps(response)
                    )
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as ex:
                logger.error(f"[AUTH] General error processing message: {ex}")
                db.rollback()
                if reply_to:
                    response = {"detail": "Internal server error."}
                    channel.basic_publish(
                        exchange='',
                        routing_key=reply_to,
                        properties=pika.BasicProperties(correlation_id=correlation_id),
                        body=json.dumps(response)
                    )
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            finally:
                db.close()

        channel.basic_consume(queue='auth_commands', on_message_callback=callback)
        logger.info("[AUTH] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"[AUTH] Error initializing consumer: {e}")
        sys.exit(1)

# Invocación de la función principal
if __name__ == "__main__":
    auth_commands_consumer()