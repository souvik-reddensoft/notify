from flask import Flask, request
import json
from unittest.mock import MagicMock
import mock # pylint:disable=E0401
from Core.Controllers.Controller import Controller
from Application.user_permissions.Controllers.UserPermissions import user_permission, UserPermission as UserPermissionClass
from Application.user_permissions.Models.UserPermissions import UserPermission
from Application.roles.Controllers.Role import Role as RoleController

app = Flask(__name__)

def testUserPermissionControllerExtendsBaseController():
    assert issubclass(UserPermissionClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfUserPermissionsModel():
    assert isinstance(user_permission.model, UserPermission) is True

def testUserPermissionControllerHasListMethod():
    assert hasattr(UserPermissionClass, 'list') is True

def testUserPermissionControllerHasCreateMethod():
    assert hasattr(UserPermissionClass, 'create') is True

def testUserPermissionControllerHasUpdateMethod():
    assert hasattr(UserPermissionClass, 'update') is True

def testUserPermissionControllerHasDeleteMethod():
    assert hasattr(UserPermissionClass, 'delete') is True

def testUserPermissionControllerHasDestroyMethod():
    assert hasattr(UserPermissionClass, 'destroy') is True

def testUserPermissionControllerHasViewMethod():
    assert hasattr(UserPermissionClass, 'view') is True

def testUserPermissionControllerHasTrashMethod():
    assert hasattr(UserPermissionClass, 'trash') is True

def testUserPermissionControllerHasRestoreMethod():
    assert hasattr(UserPermissionClass, 'restore') is True

@mock.patch.object(UserPermission, 'list')
def testUserPermissionModelListIsCalledInUserPermissionControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        user_permission.list()
        assert UserPermission().list.called # pylint: disable=E1101

@mock.patch.object(UserPermission, 'create')
def testUserPermissionModelCreateIsCalledInUserPermissionControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        user_permission.validate = _mock
        user_permission.create()
        assert user_permission.validate.called # pylint: disable=E1101
        assert UserPermission().create.called # pylint: disable=E1101

@mock.patch.object(UserPermission, 'isDeleted', return_value = None)
@mock.patch.object(UserPermission, 'update')
def testUserPermissionModelUpdateIsCalledInUserPermissionControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        user_permission.validate = _mock
        user_permission.update('1234')
        assert UserPermission().isDeleted.called # pylint: disable=E1101
        assert user_permission.validate.called # pylint: disable=E1101
        assert UserPermission().update.called # pylint: disable=E1101

@mock.patch.object(UserPermission, 'isDeleted', return_value = None)
@mock.patch.object(UserPermission, 'delete')
def testUserPermissionModelDeleteIsCalledInUserPermissionControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        user_permission.delete('1234')
        assert UserPermission().isDeleted.called # pylint: disable=E1101
        assert UserPermission().delete.called # pylint: disable=E1101

@mock.patch.object(UserPermission, 'isDeleted', return_value = {})
@mock.patch.object(UserPermission, 'restore')
def testUserPermissionModelRestoreIsCalledInUserPermissionControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        user_permission.restore('1234')
        assert UserPermission().isDeleted.called # pylint: disable=E1101
        assert UserPermission().restore.called # pylint: disable=E1101

@mock.patch.object(UserPermission, 'find', return_value = {})
@mock.patch.object(UserPermission, 'destroy', return_value = 1)
def testUserPermissionModelDestroyIsCalledInUserPermissionControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        request.environ["jwt_data"] = _mock
        user_permission.destroy('1234')
        assert UserPermission().find.called # pylint: disable=E1101
        assert UserPermission().destroy.called # pylint: disable=E1101

@mock.patch.object(RoleController, 'getDistinctPermissions', return_value = {})
@mock.patch.object(UserPermission, 'findOneUpsert', return_value = {})
def testRoleControllergetDistinctPermissionsIsCalledInUserPermissionControllersavePermissionsForThisUserAndRole(mock_getDistinctPermissions_method, mock_findoneandupsert_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        request.environ["jwt_data"] = _mock
        user_permission.savePermissionsForThisUserAndRole('634d28ab7c2b218391a183ea','634d28ab7c2b218391a183ea',['634d28ab7c2b218391a183ea'])
        assert RoleController().getDistinctPermissions.called # pylint: disable=E1101
        assert UserPermission().findOneUpsert.called # pylint: disable=E1101