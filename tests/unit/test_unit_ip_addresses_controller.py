import json
from unittest.mock import MagicMock
import mock
from flask import Flask, request
from Core.Controllers.Controller import Controller
from Application.ip_addresses.Controllers.IPAddress import iPAddress, IPAddress as IPAddressController
from Application.ip_addresses.Models.IPAddress import IPAddress
app = Flask(__name__)

def testIPAddressControllerExtendsBaseController():
    assert issubclass(IPAddressController, Controller) is True

def testIPAddressControllerHasListMethod():
    assert hasattr(IPAddressController, 'list') is True

def testIPAddressControllerHasCreateMethod():
    assert hasattr(IPAddressController, 'create') is True

def testIPAddressControllerHasUpdateMethod():
    assert hasattr(IPAddressController, 'update') is True

def testIPAddressControllerHasDeleteMethod():
    assert hasattr(IPAddressController, 'delete') is True

def testIPAddressControllerHasDestroyMethod():
    assert hasattr(IPAddressController, 'destroy') is True

def testIPAddressControllerHasViewMethod():
    assert hasattr(IPAddressController, 'view') is True

def testIPAddressControllerHasTrashMethod():
    assert hasattr(IPAddressController, 'trash') is True

def testIPAddressControllerHasRestoreMethod():
    assert hasattr(IPAddressController, 'restore') is True
    
def testExtendsBaseController():
    assert issubclass(IPAddressController, Controller) is True 

def testHasModelAttributeWhichIsInstanceOfIPAddressModel():
    assert isinstance(iPAddress.model, IPAddress) is True
    
@mock.patch.object(IPAddress, 'list')
def testIPAddressModelListIsCalledInIPAddressControllerControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        iPAddress.list()
        assert IPAddress().list.called

@mock.patch.object(IPAddress, 'create')
def testIPAddressModelCreateIsCalledInIPAddressControllerControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        iPAddress.validate = _mock
        iPAddress.create()
        assert iPAddress.validate.called
        assert IPAddress().create.called

@mock.patch.object(IPAddress, 'isDeleted', return_value = None)
@mock.patch.object(IPAddress, 'update')
def testIPAddressModelUpdateIsCalledInIPAddressControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        iPAddress.validate = _mock
        iPAddress.update('1234')
        assert iPAddress.validate.called
        assert IPAddress().isDeleted.called
        assert IPAddress().update.called

@mock.patch.object(IPAddress, 'isDeleted', return_value = None)
@mock.patch.object(IPAddress, 'delete')
def testIPAddressModelDeleteIsCalledInIPAddressControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        iPAddress.delete('1234')
        assert IPAddress().isDeleted.called
        assert IPAddress().delete.called

@mock.patch.object(IPAddress, 'isDeleted', return_value = {})
@mock.patch.object(IPAddress, 'restore')
def testIPAddressModelRestoreIsCalledInIPAddressControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        iPAddress.restore('1234')
        assert IPAddress().isDeleted.called
        assert IPAddress().restore.called

@mock.patch.object(IPAddress, 'find', return_value = {})
@mock.patch.object(IPAddress, 'destroy', return_value = 1)
def testIPAddressModelDestroyIsCalledInIPAddressControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        iPAddress.destroy('1234')
        assert IPAddress().find.called # pylint: disable=E1101
        assert IPAddress().destroy.called # pylint: disable=E1101 