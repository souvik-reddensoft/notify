from flask import Flask, request
import json
from unittest.mock import MagicMock
import mock # pylint:disable=E0401
from Core.Controllers.Controller import Controller
from Application.roles.Controllers.Role import role, Role as RoleClass
from Application.roles.Models.Role import Role

app = Flask(__name__)

def testRoleControllerExtendsBaseController():
    assert issubclass(RoleClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfRolesModel():
    assert isinstance(role.model, Role) is True

def testRoleControllerHasListMethod():
    assert hasattr(RoleClass, 'list') is True

def testRoleControllerHasCreateMethod():
    assert hasattr(RoleClass, 'create') is True

def testRoleControllerHasUpdateMethod():
    assert hasattr(RoleClass, 'update') is True

def testRoleControllerHasDeleteMethod():
    assert hasattr(RoleClass, 'delete') is True

def testRoleControllerHasDestroyMethod():
    assert hasattr(RoleClass, 'destroy') is True

def testRoleControllerHasViewMethod():
    assert hasattr(RoleClass, 'view') is True

def testRoleControllerHasTrashMethod():
    assert hasattr(RoleClass, 'trash') is True

def testRoleControllerHasRestoreMethod():
    assert hasattr(RoleClass, 'restore') is True

@mock.patch.object(Role, 'list')
def testRoleModelListIsCalledInRoleControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        role.list()
        assert Role().list.called # pylint: disable=E1101

@mock.patch.object(Role, 'create')
def testRoleModelCreateIsCalledInRoleControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        role.validate = _mock
        role.create()
        assert role.validate.called # pylint: disable=E1101
        assert Role().create.called # pylint: disable=E1101

@mock.patch.object(Role, 'isDeleted', return_value = None)
@mock.patch.object(Role, 'update')
def testRoleModelUpdateIsCalledInRoleControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        role.validate = _mock
        role.update('1234')
        assert Role().isDeleted.called # pylint: disable=E1101
        assert role.validate.called # pylint: disable=E1101
        assert Role().update.called # pylint: disable=E1101

@mock.patch.object(Role, 'isDeleted', return_value = None)
@mock.patch.object(Role, 'delete')
def testRoleModelDeleteIsCalledInRoleControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        role.delete('1234')
        assert Role().isDeleted.called # pylint: disable=E1101
        assert Role().delete.called # pylint: disable=E1101

@mock.patch.object(Role, 'isDeleted', return_value = {})
@mock.patch.object(Role, 'restore')
def testRoleModelRestoreIsCalledInRoleControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        role.restore('1234')
        assert Role().isDeleted.called # pylint: disable=E1101
        assert Role().restore.called # pylint: disable=E1101

@mock.patch.object(Role, 'find', return_value = {})
@mock.patch.object(Role, 'destroy', return_value = 1)
def testRoleModelDestroyIsCalledInRoleControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        role.destroy('1234')
        assert Role().find.called # pylint: disable=E1101
        assert Role().destroy.called # pylint: disable=E1101

@mock.patch.object(Role, 'fetchList', return_value = {"_id":"63a924d420be3234101a71ef","app_slug":"account-manager"})
def testRoleModelFetchListIsCalledInRoleControllergetPermissions(mock_fetchlist_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        role.getPermissions('1234', '1234')
        assert Role().fetchList.called # pylint: disable=E1101

@mock.patch.object(Role, 'fetchList', return_value = {"results":{"results":{"data":{"_id":"63a924d420be3234101a71ef","app_slug":"account-manager"}}}})
def testRoleModelFetchListIsCalledInRoleControllergetDistinctPermissions(mock_fetchlist_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        role.getDistinctPermissions('1234')
        assert Role().fetchList.called # pylint: disable=E1101
