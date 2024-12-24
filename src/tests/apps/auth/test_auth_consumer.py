from unittest.mock import Mock, patch
import pytest
import json
from src.apps.auth.application.consumers.auth_consumer import consume_auth_event

@pytest.fixture
def mock_channel():
    return Mock()

@pytest.fixture
def mock_method():
    mock_method = Mock()
    mock_method.delivery_tag = 123
    return mock_method

@pytest.fixture
def mock_properties():
    mock_properties = Mock()
    mock_properties.reply_to = None
    mock_properties.correlation_id = None
    return mock_properties

@pytest.fixture
def mock_message_login():
    return {"user_id": 1, "action": "login_user", "email": "test@example.com", "password": "securepassword"}

@pytest.fixture
def mock_message_sign_out():
    return {"user_id": 1, "action": "sign_out", "token": "testtoken"}

@pytest.fixture
def mock_message_unknown():
    return {"user_id": 1, "action": "unknown_action"}

def test_consume_auth_event_login(mock_channel, mock_method, mock_properties, mock_message_login):
    with patch('src.apps.auth.application.consumers.auth_consumer.handle_login_user') as mock_handle_login:
        
        mock_handle_login.return_value = {"access_token": "testtoken", "token_type": "bearer"}

        
        consume_auth_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_login))

        
        mock_handle_login.assert_called_once_with(mock_message_login, mock_channel, mock_properties)

        
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

def test_consume_auth_event_sign_out(mock_channel, mock_method, mock_properties, mock_message_sign_out):
    with patch('src.apps.auth.application.consumers.auth_consumer.handle_sign_out') as mock_handle_sign_out:
        
        mock_handle_sign_out.return_value = {"detail": "Successfully signed out."}

        
        consume_auth_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_sign_out))

        
        mock_handle_sign_out.assert_called_once_with(mock_message_sign_out, mock_channel, mock_properties)

        
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

def test_consume_auth_event_unknown_action(mock_channel, mock_method, mock_properties, mock_message_unknown):
    with patch('src.apps.auth.application.consumers.auth_consumer.handle_login_user') as mock_handle_login, \
         patch('src.apps.auth.application.consumers.auth_consumer.handle_sign_out') as mock_handle_sign_out:

        consume_auth_event(mock_channel, mock_method, mock_properties, json.dumps(mock_message_unknown))

        mock_handle_login.assert_not_called()
        mock_handle_sign_out.assert_not_called()

        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)
