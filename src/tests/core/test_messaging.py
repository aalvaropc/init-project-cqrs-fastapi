# src/tests/core/test_messaging.py

from unittest.mock import Mock
from src.core.messaging import publish_message
import json
import pika

def test_publish_message():
    mock_rabbitmq = Mock()
    mock_channel = Mock()
    mock_rabbitmq.channel.return_value = mock_channel

    message = {"key": "value"}
    queue = "test_queue"

    publish_message(mock_rabbitmq, queue, message)

    mock_rabbitmq.channel.assert_called_once()

    mock_channel.queue_declare.assert_called_once_with(queue=queue, durable=True)

    mock_channel.basic_publish.assert_called_once_with(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
