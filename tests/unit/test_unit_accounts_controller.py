import json
from unittest.mock import MagicMock
import mock
from flask import Flask, request
from Core.Controllers.Controller import Controller
from Application.accounts.Controllers.Accounts import accounts, Accounts as AccountsClass
from Application.signup.Controllers.Signup import Signup
from Application.accounts.Models.Accounts import Accounts
from Application.signin.Models.Jwt import Jwt as JwtModel
from Application.users.Models.Users import Users

app = Flask(__name__)

lock_account = {    
    "ids":["6384a32ef5ff6ec22f18cb2d"],
    "lock_duration": 3,
    "locked_indefinite":False,
    "lock_action":"lock",
    "lock_type":"days"
}

lock_indefinite = {    
    "ids":["6384a32ef5ff6ec22f18cb2d"],
    "locked_indefinite":True,
    "lock_action":"lock"
}

def testUsersControllerExtendsBaseController():
    assert issubclass(AccountsClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfAccountsModel():
    assert isinstance(accounts.model, Accounts) is True

def testUsersControllerHasListMethod():
    assert hasattr(AccountsClass, 'list') is True

def testUsersControllerHasCreateMethod():
    assert hasattr(AccountsClass, 'create') is True

def testUsersControllerHasUpdateMethod():
    assert hasattr(AccountsClass, 'update') is True

def testUsersControllerHasDeleteMethod():
    assert hasattr(AccountsClass, 'delete') is True

def testUsersControllerHasDestroyMethod():
    assert hasattr(AccountsClass, 'destroy') is True

def testUsersControllerHasViewMethod():
    assert hasattr(AccountsClass, 'view') is True

def testUsersControllerHasTrashMethod():
    assert hasattr(AccountsClass, 'trash') is True

def testUsersControllerHasRestoreMethod():
    assert hasattr(AccountsClass, 'restore') is True
    
def testExtendsBaseController():
    assert issubclass(AccountsClass, Controller) is True

@mock.patch.object(Accounts, 'list')
def testAccountsModelListIsCalledInAccountsControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        accounts.list()
        assert Accounts().list.called # pylint: disable=E1101

@mock.patch.object(Accounts, 'view', return_value = {})
def testAccountsModelViewIsCalledInAccountsControllerView(mock_view_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        accounts.view('1234')
        assert Accounts().view.called # pylint: disable=E1101

@mock.patch.object(Users, 'find', return_value = {'owner_account_id':1234, 'first_name':'test','company_name': 'test'})
@mock.patch.object(Accounts, 'find', return_value = {'_id': 1,'company_name': 'test'})
def testUsersModelFindIsCalledInAccountsControllerOverview(mock_AccountsfetchList_method, mock_usersfind_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts.overview()
        assert Users().find.called # pylint: disable=E1101
        assert Accounts().find.called # pylint: disabled=E01101

@mock.patch.object(Signup, 'create', return_value = {})
def testSignupCreateIsCalledInAccountsControllerCreate(mock_signupCreate_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts.create()
        assert Signup().create.called # pylint: disable=E1101

@mock.patch.object(Signup, 'update', return_value = {})
def testSignupUpdateIsCalledInAccountsControllerUpdate(mock_signupUpdate_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts.update('1234')
        assert Signup().update.called # pylint: disable=E1101

@mock.patch.object(JwtModel, 'activeUserCount', return_value = {})
def testSignupUpdateIsCalledInAccountsControllerUpdate(mock_signupUpdate_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts.activeUsers()
        assert JwtModel().activeUserCount.called # pylint: disable=E1101

@mock.patch.object(Accounts, 'fetchList')
def testAccountsModelfetchListIsCalledInAccountsControllerList(mock_fetchList_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        accounts.list()
        assert Accounts().fetchList.called

@mock.patch.object(Accounts, 'manageAccountstatus', return_value = None)
def testAccountModelManageAccountsCalledInAccountControllerManageAccountForUnlock(mock_manage_accountLocks):
    with app.test_request_context(data = json.dumps({"lock_action":'unlock', "ids":["6384a32ef5ff6ec22f18cb2d"]}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        accounts.validate = _mock
        accounts.updateAccountLock()
        assert accounts.validate.called
        assert Accounts().manageAccountstatus.called

@mock.patch.object(Accounts, 'manageAccountstatus', return_value = None)
def testAccountModelManageAccountsCalledInAccountControllerManageAccountForLock(mock_manage_accountLocks):
    with app.test_request_context(data = json.dumps(lock_account), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        accounts.validate = _mock
        accounts.updateAccountLock()
        assert accounts.validate.called
        assert Accounts().manageAccountstatus.called  

@mock.patch.object(Accounts, 'manageAccountstatus', return_value = None)
def testAccountModelManageAccountsCalledInAccountControllerManageAccountForIndefiniteLock(mock_manage_accountLocks):
    with app.test_request_context(data = json.dumps(lock_indefinite), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        accounts.validate = _mock
        accounts.updateAccountLock()
        assert accounts.validate.called
        assert Accounts().manageAccountstatus.called        
