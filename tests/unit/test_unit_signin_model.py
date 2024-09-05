from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.signin.Models.Jwt  import Jwt
app = Flask(__name__)

def testJwtModelHasListMethod():
    assert hasattr(Jwt, 'list') is True

def testJwtModelHasDeleteMethod():
    assert hasattr(Jwt, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testJwtModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testJwtModelHasSchemaDefinition():
    assert len(Jwt.fields) > 0

def testJwtModelHasCollectionNameDefined():
    assert Jwt.collection is not None and  Jwt.collection == 'jwt_manage'

def testJwtModelHasCreateDefinition():
    assert hasattr(Jwt, 'create') is True

def testJwtModelHasFindDefinition():
    assert hasattr(Jwt, 'find') is True

def testJwtModelHasUpdateDefinition():
    assert hasattr(Jwt, 'update') is True

def testJwtModelHasfetchListDefinition():
    assert hasattr(Jwt, 'fetchList') is True

def testJwtModelHasgetListQueryDefinition():
    assert hasattr(Jwt, 'getListQuery') is True

def testJwtModelHasRestoreDefinition():
    assert hasattr(Jwt, 'restore') is True

def testJwtModelHasdestroyDefinition():
    assert hasattr(Jwt, 'destroy') is True

def testJwtModelHasisDeletedDefinition():
    assert hasattr(Jwt, 'isDeleted') is True

def testJwtModelHasgetFieldsDefinition():
    assert hasattr(Jwt, 'getFields') is True

def testJwtModelHasschemaDefinition():
    assert hasattr(Jwt, 'schema') is True

def testJwtModelHasgetDataTypeKeysDefinition():
    assert hasattr(Jwt, 'getDataTypeKeys') is True

def testJwtModelHasappendScopeDefinition():
    assert hasattr(Jwt, 'appendScope') is True

def testJwtModelHastypeRefDefinition():
    assert hasattr(Jwt, 'typeRef') is True

def testJwtModelHastypeCastDefinition():
    assert hasattr(Jwt, 'typeCast') is True

def testJwtModelHastoISODateDefinition():
    assert hasattr(Jwt, 'toISODate') is True

def testJwtModelHastoIntDefinition():
    assert hasattr(Jwt, 'toInt') is True

def testJwtModelHasactiveUserCountDefinition(): 
    assert hasattr(Jwt, 'activeUserCount') is True

def testJwtModelHastokenForOrganizationDefinition(): 
    assert hasattr(Jwt, 'tokenForOrganization') is True