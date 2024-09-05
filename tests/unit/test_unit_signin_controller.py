from flask import Flask, request
import json
from unittest.mock import MagicMock
from hashlib import md5
import mock # pylint:disable=E0401
from Application.signin.Helpers import Helper
from Core.Controllers.Controller import Controller
from Application.signin.Controllers.Signin import sign_in, Signin as SigninClass
from Application.signin.Models.Jwt import Jwt
from Application.signin.Services.SigninService import (SigninException,
                                                       SigninService)
app = Flask(__name__)

def testSigninControllerExtendsBaseController():
    assert issubclass(SigninClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfRolesModel():
    assert isinstance(sign_in.model, Jwt) is True

def testSigninControllerHasListMethod():
    assert hasattr(SigninClass, 'list') is True

def testSigninControllerHasCreateMethod():
    assert hasattr(SigninClass, 'create') is True

def testSigninControllerHasUpdateMethod():
    assert hasattr(SigninClass, 'update') is True

def testSigninControllerHasDeleteMethod():
    assert hasattr(SigninClass, 'delete') is True

def testSigninControllerHasDestroyMethod():
    assert hasattr(SigninClass, 'destroy') is True

def testSigninControllerHasViewMethod():
    assert hasattr(SigninClass, 'view') is True

def testSigninControllerHasTrashMethod():
    assert hasattr(SigninClass, 'trash') is True

def testSigninControllerHasRestoreMethod():
    assert hasattr(SigninClass, 'restore') is True

@mock.patch.object(Jwt, 'list')
def testJwtModelListIsCalledInSigninControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        sign_in.list()
        assert Jwt().list.called # pylint: disable=E1101

# @mock.patch.object(SigninService, 'initUser', return_value={})
# @mock.patch.object(SigninService, 'checkUnknownDevice', return_value={})
# @mock.patch.object(SigninService, 'generateToken', return_value={})
# @mock.patch.object(SigninService, 'removeUnwantedDevices', return_value={})
# def testSigninServiceIsCalledInSigninControllerCreate(mock_signinclass_inituser_method, mock_checkUnknownDevice_method, mock_generateToken_method, mock_removeUnwantedDevices_method):
#     with app.test_request_context(data = json.dumps({
#   "email": "saptarshi.bagchi@codeclouds.com",
# "remember_me": False,
# "password":"Test@1234",
# "host_data": {"fingerprint": "9e8ce2a57b80b51f3b64c0ac64eb324c2"}
# }), content_type='application/json'):
#         _mock = MagicMock()
#         request.environ["jwt_data"] = _mock
#         request.t = _mock
#         sign_in.validate = _mock
#         sign_in.create()
#         assert sign_in.validate.called # pylint: disable=E1101
#         assert SigninService().initUser.called
#         assert SigninService().checkUnknownDevice.called
#         assert SigninService().generateToken.called
#         assert SigninService().removeUnwantedDevices.called

@mock.patch.object(Jwt, 'isDeleted', return_value = None)
@mock.patch.object(Jwt, 'update')
def testJwtModelUpdateIsCalledInSigninControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        sign_in.validate = _mock
        sign_in.update('1234')
        assert Jwt().isDeleted.called # pylint: disable=E1101
        assert sign_in.validate.called # pylint: disable=E1101
        assert Jwt().update.called # pylint: disable=E1101

@mock.patch.object(Jwt, 'isDeleted', return_value = None)
@mock.patch.object(Jwt, 'delete')
def testJwtModelDeleteIsCalledInSigninControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        sign_in.delete('1234')
        assert Jwt().isDeleted.called # pylint: disable=E1101
        assert Jwt().delete.called # pylint: disable=E1101

@mock.patch.object(Jwt, 'isDeleted', return_value = {})
@mock.patch.object(Jwt, 'restore')
def testJwtModelRestoreIsCalledInSigninControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        sign_in.restore('1234')
        assert Jwt().isDeleted.called # pylint: disable=E1101
        assert Jwt().restore.called # pylint: disable=E1101

@mock.patch.object(Jwt, 'find', return_value = {})
@mock.patch.object(Jwt, 'destroy', return_value = 1)
def testJwtModelDestroyIsCalledInSigninControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        sign_in.destroy('1234')
        assert Jwt().find.called # pylint: disable=E1101
        assert Jwt().destroy.called # pylint: disable=E1101

# @mock.patch.object(SigninService, 'initUser', return_value={})
# @mock.patch.object(Helper, 'sendUnknownDeviceNotification', return_value={})
# def testSigninServiceIsCalledInSigninControllerresendUnknownDeviceNotification(mock_signinclass_inituser_method, mock_sendUnknownDeviceNotification_method):
#     with app.test_request_context(data = json.dumps({"email": "saptarshi.bagchi@codeclouds.com","remember_me": False,"password":"Test@1234","host_data": {"fingerprint": "9e8ce2a57b80b51f3b64c0ac64eb324c2"}}), content_type='application/json'):
#         _mock = MagicMock()
#         request.environ["jwt_data"] = _mock
#         request.t = _mock
#         sign_in.validate = _mock
#         sign_in.create()
#         assert sign_in.validate.called # pylint: disable=E1101
#         assert SigninService().initUser.called
#         assert Helper().sendUnknownDeviceNotification.called
