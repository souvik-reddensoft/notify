import json
from unittest.mock import Mock, MagicMock
import mock
from Core.Boot.Bus import MessageBus
from Application.users.Helpers.NotificationManage import NotificationManage
from flask import Flask, request
app = Flask(__name__)

def testNotificationHassendMethod():
    assert hasattr(NotificationManage, 'send') is True
    
@mock.patch.object(MessageBus, 'produce', return_value = {})
def testUsersNotificationCalledProduceMethod(mock_produce_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        notification_data = _mock
        NotificationManage.send(notification_data)
        assert MessageBus.produce.called

@mock.patch.object(MessageBus, 'produce', return_value = {})       
def testUsersHashPasswordReturnsInstanceOfString(mock_produce_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        notification_data = _mock
        assert NotificationManage.send(notification_data) is None