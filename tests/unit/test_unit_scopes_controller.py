from flask import Flask, request
import json
from unittest.mock import MagicMock
import mock # pylint:disable=E0401
from Core.Controllers.Controller import Controller
from Application.scopes.Controllers.Scope import scope, Scope as ScopeClass
from Application.scopes.Models.Scope import Scope

app = Flask(__name__)

def testScopeControllerExtendsBaseController():
    assert issubclass(ScopeClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfScopeModel():
    assert isinstance(scope.model, Scope) is True

def testScopeControllerHasListMethod():
    assert hasattr(ScopeClass, 'list') is True

def testScopeControllerHasCreateMethod():
    assert hasattr(ScopeClass, 'create') is True

def testScopeControllerHasUpdateMethod():
    assert hasattr(ScopeClass, 'update') is True

def testScopeControllerHasDeleteMethod():
    assert hasattr(ScopeClass, 'delete') is True

def testScopeControllerHasDestroyMethod():
    assert hasattr(ScopeClass, 'destroy') is True

def testScopeControllerHasViewMethod():
    assert hasattr(ScopeClass, 'view') is True

def testScopeControllerHasTrashMethod():
    assert hasattr(ScopeClass, 'trash') is True

def testScopeControllerHasRestoreMethod():
    assert hasattr(ScopeClass, 'restore') is True

@mock.patch.object(Scope, 'list')
def testScopeModelListIsCalledInScopeControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        scope.list()
        assert Scope().list.called # pylint: disable=E1101

@mock.patch.object(Scope, 'create')
def testScopeModelCreateIsCalledInScopeControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        scope.validate = _mock
        scope.create()
        assert scope.validate.called # pylint: disable=E1101
        assert Scope().create.called # pylint: disable=E1101

@mock.patch.object(Scope, 'isDeleted', return_value = None)
@mock.patch.object(Scope, 'update')
def testScopeModelUpdateIsCalledInScopeControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        scope.validate = _mock
        scope.update('1234')
        assert Scope().isDeleted.called # pylint: disable=E1101
        assert scope.validate.called # pylint: disable=E1101
        assert Scope().update.called # pylint: disable=E1101

@mock.patch.object(Scope, 'isDeleted', return_value = None)
@mock.patch.object(Scope, 'delete')
def testScopeModelDeleteIsCalledInScopeControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        scope.delete('1234')
        assert Scope().isDeleted.called # pylint: disable=E1101
        assert Scope().delete.called # pylint: disable=E1101

@mock.patch.object(Scope, 'isDeleted', return_value = {})
@mock.patch.object(Scope, 'restore')
def testScopeModelRestoreIsCalledInScopeControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        scope.restore('1234')
        assert Scope().isDeleted.called # pylint: disable=E1101
        assert Scope().restore.called # pylint: disable=E1101

@mock.patch.object(Scope, 'find', return_value = {})
@mock.patch.object(Scope, 'destroy', return_value = 1)
def testScopeModelDestroyIsCalledInScopeControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        scope.destroy('1234')
        assert Scope().find.called # pylint: disable=E1101
        assert Scope().destroy.called # pylint: disable=E1101
