from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.user_permissions.Models.UserPermissions  import UserPermission
app = Flask(__name__)

def testUserPermissionModelHasListMethod():
    assert hasattr(UserPermission, 'list') is True

def testUserPermissionModelHasDeleteMethod():
    assert hasattr(UserPermission, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testUserPermissionModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testUserPermissionModelHasSchemaDefinition():
    assert len(UserPermission.fields) > 0

def testUserPermissionModelHasCollectionNameDefined():
    assert UserPermission.collection is not None and  UserPermission.collection == 'user_permissions'

def testUserPermissionModelHasCreateDefinition():
    assert hasattr(UserPermission, 'create') is True

def testUserPermissionModelHasFindDefinition():
    assert hasattr(UserPermission, 'find') is True

def testUserPermissionModelHasUpdateDefinition():
    assert hasattr(UserPermission, 'update') is True

def testUserPermissionModelHasfetchListDefinition():
    assert hasattr(UserPermission, 'fetchList') is True

def testUserPermissionModelHasgetListQueryDefinition():
    assert hasattr(UserPermission, 'getListQuery') is True

def testUserPermissionModelHasRestoreDefinition():
    assert hasattr(UserPermission, 'restore') is True

def testUserPermissionModelHasdestroyDefinition():
    assert hasattr(UserPermission, 'destroy') is True

def testUserPermissionModelHasisDeletedDefinition():
    assert hasattr(UserPermission, 'isDeleted') is True

def testUserPermissionModelHasgetFieldsDefinition():
    assert hasattr(UserPermission, 'getFields') is True

def testUserPermissionModelHasschemaDefinition():
    assert hasattr(UserPermission, 'schema') is True

def testUserPermissionModelHasgetDataTypeKeysDefinition():
    assert hasattr(UserPermission, 'getDataTypeKeys') is True

def testUserPermissionModelHasappendScopeDefinition():
    assert hasattr(UserPermission, 'appendScope') is True

def testUserPermissionModelHastypeRefDefinition():
    assert hasattr(UserPermission, 'typeRef') is True

def testUserPermissionModelHastypeCastDefinition():
    assert hasattr(UserPermission, 'typeCast') is True

def testUserPermissionModelHastoISODateDefinition():
    assert hasattr(UserPermission, 'toISODate') is True

def testUserPermissionModelHastoIntDefinition():
    assert hasattr(UserPermission, 'toInt') is True

def testUserPermissionModelHasremoveAllPermissionsOfThisOrganizationDefinition():
    assert hasattr(UserPermission, 'removeAllPermissionsOfThisOrganization') is True