from unittest.mock import Mock, patch
import pytest
import json
from src.apps.users.application.consumers.user_consumer import consume_user_event

@pytest.fixture
def mock_channel():
    return Mock()

@pytest.fixture
def mock_method():
    mock_method = Mock()
    mock_method.delivery_tag = 456
    return mock_method

@pytest.fixture
def mock_properties():
    mock_properties = Mock()
    mock_properties.reply_to = None
    mock_properties.correlation_id = None
    return mock_properties

@pytest.fixture
def mock_message_create():
    return {
        "user_id": 1,
        "action": "create_user",
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    }

@pytest.fixture
def mock_message_update():
    return {
        "user_id": 1,
        "action": "update_user",
        "name": "Updated Name",
        "email": "updated@example.com"
    }

@pytest.fixture
def mock_message_delete():
    return {
        "user_id": 1,
        "action": "delete_user"
    }

@pytest.fixture
def mock_message_unknown():
    return {
        "user_id": 1,
        "action": "unknown_action"
    }

def test_consume_user_event_create(mock_channel, mock_method, mock_properties, mock_message_create):
    with patch('src.apps.users.application.consumers.user_consumer.handle_create_user') as mock_handle_create:
        mock_handle_create.return_value = None
        consume_user_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_create))
        mock_handle_create.assert_called_once_with(mock_channel, mock_message_create)
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

def test_consume_user_event_update(mock_channel, mock_method, mock_properties, mock_message_update):
    with patch('src.apps.users.application.consumers.user_consumer.handle_update_user') as mock_handle_update:
        mock_handle_update.return_value = None
        consume_user_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_update))
        mock_handle_update.assert_called_once_with(mock_channel, mock_message_update)
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

def test_consume_user_event_delete(mock_channel, mock_method, mock_properties, mock_message_delete):
    with patch('src.apps.users.application.consumers.user_consumer.handle_delete_user') as mock_handle_delete:
        mock_handle_delete.return_value = None
        consume_user_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_delete))
        mock_handle_delete.assert_called_once_with(mock_channel, mock_message_delete)
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

def test_consume_user_event_unknown_action(mock_channel, mock_method, mock_properties, mock_message_unknown):
    with patch('src.apps.users.application.consumers.user_consumer.handle_create_user') as mock_handle_create, \
         patch('src.apps.users.application.consumers.user_consumer.handle_update_user') as mock_handle_update, \
         patch('src.apps.users.application.consumers.user_consumer.handle_delete_user') as mock_handle_delete:

        consume_user_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_unknown))

        mock_handle_create.assert_not_called()
        mock_handle_update.assert_not_called()
        mock_handle_delete.assert_not_called()

        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)
