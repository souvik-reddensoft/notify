from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.roles.Models.Role  import Role
app = Flask(__name__)

def testRoleModelHasListMethod():
    assert hasattr(Role, 'list') is True

def testRoleModelHasDeleteMethod():
    assert hasattr(Role, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testRoleModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testRoleModelHasSchemaDefinition():
    assert len(Role.fields) > 0

def testRoleModelHasCollectionNameDefined():
    assert Role.collection is not None and  Role.collection == 'roles'

def testRoleModelHasCreateDefinition():
    assert hasattr(Role, 'create') is True

def testRoleModelHasFindDefinition():
    assert hasattr(Role, 'find') is True

def testRoleModelHasUpdateDefinition():
    assert hasattr(Role, 'update') is True

def testRoleModelHasfetchListDefinition():
    assert hasattr(Role, 'fetchList') is True

def testRoleModelHasgetListQueryDefinition():
    assert hasattr(Role, 'getListQuery') is True

def testRoleModelHasRestoreDefinition():
    assert hasattr(Role, 'restore') is True

def testRoleModelHasdestroyDefinition():
    assert hasattr(Role, 'destroy') is True

def testRoleModelHasisDeletedDefinition():
    assert hasattr(Role, 'isDeleted') is True

def testRoleModelHasgetFieldsDefinition():
    assert hasattr(Role, 'getFields') is True

def testRoleModelHasschemaDefinition():
    assert hasattr(Role, 'schema') is True

def testRoleModelHasgetDataTypeKeysDefinition():
    assert hasattr(Role, 'getDataTypeKeys') is True

def testRoleModelHasappendScopeDefinition():
    assert hasattr(Role, 'appendScope') is True

def testRoleModelHastypeRefDefinition():
    assert hasattr(Role, 'typeRef') is True

def testRoleModelHastypeCastDefinition():
    assert hasattr(Role, 'typeCast') is True

def testRoleModelHastoISODateDefinition():
    assert hasattr(Role, 'toISODate') is True

def testRoleModelHastoIntDefinition():
    assert hasattr(Role, 'toInt') is True