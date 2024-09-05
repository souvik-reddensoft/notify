from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.scopes.Models.Scope  import Scope
app = Flask(__name__)

def testScopeModelHasListMethod():
    assert hasattr(Scope, 'list') is True

def testScopeModelHasDeleteMethod():
    assert hasattr(Scope, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testScopeModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testScopeModelHasSchemaDefinition():
    assert len(Scope.fields) > 0

def testScopeModelHasCollectionNameDefined():
    assert Scope.collection is not None and  Scope.collection == 'scopes'

def testScopeModelHasCreateDefinition():
    assert hasattr(Scope, 'create') is True

def testScopeModelHasFindDefinition():
    assert hasattr(Scope, 'find') is True

def testScopeModelHasUpdateDefinition():
    assert hasattr(Scope, 'update') is True

def testScopeModelHasfetchListDefinition():
    assert hasattr(Scope, 'fetchList') is True

def testScopeModelHasgetListQueryDefinition():
    assert hasattr(Scope, 'getListQuery') is True

def testScopeModelHasRestoreDefinition():
    assert hasattr(Scope, 'restore') is True

def testScopeModelHasdestroyDefinition():
    assert hasattr(Scope, 'destroy') is True

def testScopeModelHasisDeletedDefinition():
    assert hasattr(Scope, 'isDeleted') is True

def testScopeModelHasgetFieldsDefinition():
    assert hasattr(Scope, 'getFields') is True

def testScopeModelHasschemaDefinition():
    assert hasattr(Scope, 'schema') is True

def testScopeModelHasgetDataTypeKeysDefinition():
    assert hasattr(Scope, 'getDataTypeKeys') is True

def testScopeModelHasappendScopeDefinition():
    assert hasattr(Scope, 'appendScope') is True

def testScopeModelHastypeRefDefinition():
    assert hasattr(Scope, 'typeRef') is True

def testScopeModelHastypeCastDefinition():
    assert hasattr(Scope, 'typeCast') is True

def testScopeModelHastoISODateDefinition():
    assert hasattr(Scope, 'toISODate') is True

def testScopeModelHastoIntDefinition():
    assert hasattr(Scope, 'toInt') is True