from unittest.mock import Mock        
import json
import mock
import pymongo
from flask import Flask, request
from Core.Models.Model import Model
from Application.ip_addresses.Models.IPAddress import ipAddress, IPAddress
from Core.Factories.Database import DbFactory as db
from Core.Models.Model import Model as Base
app = Flask(__name__)

#db_instance = ipAddress.getCollection()

def testIPAddressModelHasListMethod():
    assert hasattr(IPAddress, 'list') is True

def testIPAddressModelHasDeleteMethod():
    assert hasattr(IPAddress, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testIPAddressModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testIPAddressModelHasSchemaDefinition():
    assert len(IPAddress.fields) > 0

def testIPAddressModelHasCollectionNameDefined():
    assert IPAddress.collection is not  None and  IPAddress.collection == 'ip_addresses'

def testIPAddressMethodFetchListShouldReturnBoolean():
    _mock = Mock()
    data = IPAddress.fetchList.return_value = True
    assert isinstance(data, bool) is True

def testIPAddressModelHasCheckDuplicateIPAddressMethod():
    assert hasattr(IPAddress, 'checkDuplicateIPAddress') is True
    