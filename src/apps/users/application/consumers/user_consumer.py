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


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("user_consumer")

def user_commands_consumer():
    """
    Consumer para la cola 'users_commands'.
    Maneja create/update/delete de usuarios de forma asíncrona.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='users_commands', durable=True)
        logger.info("[USERS] Connected to RabbitMQ and declared queue 'users_commands'.")

        def callback(ch, method, properties, body):
            logger.info(f"[USERS] Received message: {body}")
            data = json.loads(body)
            action = data.get("action")
            db: Session = SessionLocalWriter()

            try:
                repo = UserRepositoryWriter(db)

                if action == "create_user":
                    logger.info("Processing create_user action")
                    use_case = CreateUserUseCase(repo)
                    use_case.execute(
                        name=data["name"],
                        email=data["email"],
                        password=data["password"]
                    )
                elif action == "update_user":
                    logger.info("Processing update_user action")
                    use_case = UpdateUserUseCase(repo)
                    use_case.execute(
                        user_id=data["user_id"],
                        name=data["name"],
                        email=data["email"]
                    )
                elif action == "delete_user":
                    logger.info("Processing delete_user action")
                    use_case = DeleteUserUseCase(repo)
                    use_case.execute(user_id=data["user_id"])
                else:
                    logger.warning(f"Unknown action: {action}")

                db.commit()
                logger.info(f"[USERS] Successfully processed action: {action}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as ex:
                logger.error(f"[USERS] Error processing message: {ex}")
                db.rollback()
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            finally:
                db.close()

        channel.basic_consume(queue='users_commands', on_message_callback=callback)
        logger.info("[USERS] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"[USERS] Error initializing consumer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    user_commands_consumer()
