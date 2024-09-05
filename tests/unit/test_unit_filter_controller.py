import json
from unittest.mock import Mock, MagicMock
import mock
from flask import Flask, request
from werkzeug.exceptions import NotFound
from Application.filter.Models.Filter import Filter
from Application.filter.Controllers.Filter import accounts_filter
from Core.Controllers.Controller import Controller
app = Flask(__name__)

def testFilterControllerHasListMethod():
    assert hasattr(accounts_filter, 'list') is True

def testFilterControllerHasCreateMethod():
    assert hasattr(accounts_filter, 'create') is True

def testFilterControllerHasUpdateMethod():
    assert hasattr(accounts_filter, 'update') is True

def testFilterControllerHasViewMethod():
    assert hasattr(accounts_filter, 'view') is True

@mock.patch.object(Controller, '__init__',return_value = None)
def testFilterControllerHasBaseControllerExtended(mock_base_method):
    assert Controller().__init__.called

@mock.patch.object(Filter, 'create')
def testFilterControllerCreateMethodCalledWithValidation(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts_filter.validate = _mock
        accounts_filter.create()
        assert accounts_filter.validate.called

@mock.patch.object(Filter, 'create')
def testFilterControllerCreateMethodCalledWithBaseCreateMethod(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts_filter.validate = _mock
        accounts_filter.create()
        assert Filter().create.called

def testFilterControllerHasModelInstance():
    assert isinstance(accounts_filter.model, Filter) is True

@mock.patch.object(Controller, 'view')
def testFilterControllerViewMethodCalledBaseViewMethod(mock_view_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = Mock()
        accounts_filter.view("507f1f77bcf86cd799439011")
        assert Controller().view.called

@mock.patch.object(Filter, 'list')
def testFilterControllerListMethodCalledModelFilterListMethod(mock_List_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts_filter.list()
        assert Filter().list.called

@mock.patch.object(Filter, 'isDeleted')
def testFilterControllerUpdateMethodThrowException(mock_is_deleted):
    with app.test_request_context(data=json.dumps({}), content_type='application/json'):
        try:
            _mock = Mock()
            accounts_filter.update("507f1f77bcf86cd799439011")
            assert False
        except NotFound:
            assert True

@mock.patch.object(Filter, 'isDeleted', return_value = None)
@mock.patch.object(Filter, 'update')
def testFilterControllerUpdateMethodCalledBaseUpdateMethod(mock_update_method, mock_is_deleted):
    with app.test_request_context(data=json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        accounts_filter.validate = _mock
        accounts_filter.update("507f1f77bcf86cd799439011")
        assert Filter().update.called

@mock.patch.object(Filter, 'find', return_value = {})
@mock.patch.object(Filter, 'destroy', return_value = 1)
def testFilterModelDestroyIsCalledInFilterControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = Mock()
        request.t = _mock
        accounts_filter.destroy('507f1f77bcf86cd799439011')
        assert Filter().find.called
        assert Filter().destroy.called
