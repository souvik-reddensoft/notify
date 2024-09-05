import json
# from Core.Helpers import Helper
from Application.signin.Helpers import Helper
import mock
from Core.Factories.Database import DbFactory
from Application.users.Helpers.NotificationManage import NotificationManage
from unittest.mock import MagicMock
from Application.users.Models.Users import users
from flask import Flask
import datetime

app = Flask(__name__)

def testSigninHelper():
    assert Helper().maskPhoneNumber("9830562552", 3) == "***0562552"
    assert Helper().maskPhoneNumber("9830562552", 11) == "*830562552"
    assert Helper().maskPhoneNumber("9830562552", 0) == "9830562552"

# Base Cases
@mock.patch.object(NotificationManage, 'send', return_value= {})    
def testUnknownDeviceNotificationSenderHelper(argument):
   assert Helper.sendUnknownDeviceNotification({}, {}) is None
   assert Helper.sendUnknownDeviceNotification({'unknown_devices': []}, {}) is None
   assert not NotificationManage.send.called



@mock.patch.object(NotificationManage, 'send', return_value= {}) 
@mock.patch.object(users, 'update', return_value = True)
def testUnknownDeviceNotificationIsSent(_, _2):
   user_data = {
       '_id': 123,
       'email': 'roni.bagchi@gmail.com',
       'first_name': 'Saptarshi',
       'last_name': 'Bagchi',
       'unknown_devices': [
           {
               'otp': 312234,
               'host_data': {
                   'fingerprint': 'test'
               }
           }
       ],
   }
   with app.test_request_context(data = json.dumps({})):
        Helper.sendUnknownDeviceNotification(user_data, { 'fingerprint': 'test'})
        assert NotificationManage.send.called
        assert users.update.called



@mock.patch.object(NotificationManage, 'send', return_value= {})
def testUnknownDeviceNotificationIsNotSent(_):
   print(_)
   user_data = {
       '_id': 123,
       'email': 'roni.bagchi@gmail.com',
       'first_name': 'Saptarshi',
       'last_name': 'Bagchi',
       'unknown_devices': [
           {
               'otp': 312234,
               'host_data': {
                   'fingerprint': 'test'
               },
               'last_sent': datetime.datetime.now() - datetime.timedelta(seconds=-10)
           }
       ],
   }
   with app.test_request_context(data = json.dumps({})):
        Helper.sendUnknownDeviceNotification(user_data, { 'fingerprint': 'test'})
        assert not NotificationManage.send.called

   