from flask import Flask, request
import json
from unittest.mock import MagicMock
import mock # pylint:disable=E0401
from Core.Controllers.Controller import Controller
from Application.signup.Controllers.Signup import signup, Signup as SignupClass
from Application.signup.Models.Signup import Signup
from Application.accounts.Models.Accounts import Accounts
from Application.users.Models.Users import Users
from Application.signup.Helpers import Helper as SignupHelper

app = Flask(__name__)

def testSignupControllerExtendsBaseController():
    assert issubclass(SignupClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfSignupModel():
    assert isinstance(signup.model, Signup) is True

def testSignupControllerHasListMethod():
    assert hasattr(SignupClass, 'list') is True

def testSignupControllerHasCreateMethod():
    assert hasattr(SignupClass, 'create') is True

def testSignupControllerHasUpdateMethod():
    assert hasattr(SignupClass, 'update') is True

def testSignupControllerHasDeleteMethod():
    assert hasattr(SignupClass, 'delete') is True

def testSignupControllerHasDestroyMethod():
    assert hasattr(SignupClass, 'destroy') is True

def testSignupControllerHasViewMethod():
    assert hasattr(SignupClass, 'view') is True

def testSignupControllerHasTrashMethod():
    assert hasattr(SignupClass, 'trash') is True

def testSignupControllerHasRestoreMethod():
    assert hasattr(SignupClass, 'restore') is True

@mock.patch.object(Signup, 'list')
def testSignupModelListIsCalledInSignupControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        signup.list()
        assert Signup().list.called # pylint: disable=E1101

@mock.patch.object(Signup, 'create')
def testSignupModelCreateIsCalledInSignupControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        signup.validate = _mock
        signup.create()
        assert signup.validate.called # pylint: disable=E1101
        assert Signup().create.called # pylint: disable=E1101

@mock.patch.object(Accounts, 'update', return_value = 1)
@mock.patch.object(Users, 'update', return_value = 1)
@mock.patch.object(Users, 'fetchList', return_value={'results':{'results_count':1, 'results':{'data':[{'first_name':'Test Firstname'}]}}})
def testAccountsModelUpdateIsCalledInSignupControllerUpdate(mock_fetchlist_method, mock_accountsupdate_method, mock_usersupdate_method):
    with app.test_request_context(data = json.dumps({"company_name":"ABCD Pvt Ltd."}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        signup.validate = _mock
        signup.update('63aab38e90e031375a6cf0f8')
        assert signup.validate.called # pylint: disable=E1101
        assert Accounts().update.called # pylint: disable=E1101
        assert Users().fetchList.called

@mock.patch.object(Signup, 'isDeleted', return_value = None)
@mock.patch.object(Signup, 'delete')
def testSignupModelDeleteIsCalledInSignupControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        signup.delete('1234')
        assert Signup().isDeleted.called # pylint: disable=E1101
        assert Signup().delete.called # pylint: disable=E1101

@mock.patch.object(Signup, 'isDeleted', return_value = {})
@mock.patch.object(Signup, 'restore')
def testSignupModelRestoreIsCalledInSignupControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        signup.restore('1234')
        assert Signup().isDeleted.called # pylint: disable=E1101
        assert Signup().restore.called # pylint: disable=E1101

@mock.patch.object(Signup, 'find', return_value = {})
@mock.patch.object(Signup, 'destroy', return_value = 1)
def testSignupModelDestroyIsCalledInSignupControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        signup.destroy('1234')
        assert Signup().find.called # pylint: disable=E1101
        assert Signup().destroy.called # pylint: disable=E1101

# @mock.patch.object(SignupHelper, 'sendVerificationEmail', return_value = {})
# @mock.patch.object(SignupHelper, 'generateVerificationHash', return_value = {})
# @mock.patch.object(Users, 'fetchList', return_value = {'results':{'results_count':1,'results':{'data':[{'status':1}]}}})
# def testUsersModelFetchlistIsCalledInSignupControllersendVerificationEmail(mock_fetchlist_method, mock_generateverificationhash_method,mock_sendverificationemail_method):
#     with app.test_request_context():
#         _mock = MagicMock()
#         request.t = _mock
#         signup.sendVerificationEmail()
#         assert Users().fetchList.called # pylint: disable=E1101
#         assert SignupHelper().sendInvitationEmail.called
