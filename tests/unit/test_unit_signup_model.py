from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.signup.Models.Signup  import Signup
app = Flask(__name__)

def testSignupModelHasListMethod():
    assert hasattr(Signup, 'list') is True

def testSignupModelHasDeleteMethod():
    assert hasattr(Signup, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testSignupModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testSignupModelHasSchemaDefinition():
    assert len(Signup.fields) > 0

def testSignupModelHasCreateDefinition():
    assert hasattr(Signup, 'create') is True

def testSignupModelHasFindDefinition():
    assert hasattr(Signup, 'find') is True

def testSignupModelHasUpdateDefinition():
    assert hasattr(Signup, 'update') is True

def testSignupModelHasfetchListDefinition():
    assert hasattr(Signup, 'fetchList') is True

def testSignupModelHasgetListQueryDefinition():
    assert hasattr(Signup, 'getListQuery') is True

def testSignupModelHasRestoreDefinition():
    assert hasattr(Signup, 'restore') is True

def testSignupModelHasdestroyDefinition():
    assert hasattr(Signup, 'destroy') is True

def testSignupModelHasisDeletedDefinition():
    assert hasattr(Signup, 'isDeleted') is True

def testSignupModelHasgetFieldsDefinition():
    assert hasattr(Signup, 'getFields') is True

def testSignupModelHasschemaDefinition():
    assert hasattr(Signup, 'schema') is True

def testSignupModelHasgetDataTypeKeysDefinition():
    assert hasattr(Signup, 'getDataTypeKeys') is True

def testSignupModelHasappendScopeDefinition():
    assert hasattr(Signup, 'appendScope') is True

def testSignupModelHastypeRefDefinition():
    assert hasattr(Signup, 'typeRef') is True

def testSignupModelHastypeCastDefinition():
    assert hasattr(Signup, 'typeCast') is True

def testSignupModelHastoISODateDefinition():
    assert hasattr(Signup, 'toISODate') is True

def testSignupModelHastoIntDefinition():
    assert hasattr(Signup, 'toInt') is True