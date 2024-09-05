from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.feedback.Models.Feedback  import Feedback
app = Flask(__name__)

def testFeedbackModelHasListMethod():
    assert hasattr(Feedback, 'list') is True

def testFeedbackModelHasDeleteMethod():
    assert hasattr(Feedback, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testFeedbackModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testFeedbackModelHasSchemaDefinition():
    assert len(Feedback.fields) > 0

def testFeedbackModelHasCollectionNameDefined():
    assert Feedback.collection is not None and  Feedback.collection == 'feedbacks'

def testFeedbackModelHasCreateDefinition():
    assert hasattr(Feedback, 'create') is True

def testFeedbackModelHasFindDefinition():
    assert hasattr(Feedback, 'find') is True

def testFeedbackModelHasUpdateDefinition():
    assert hasattr(Feedback, 'update') is True

def testFeedbackModelHasfetchListDefinition():
    assert hasattr(Feedback, 'fetchList') is True

def testFeedbackModelHasgetListQueryDefinition():
    assert hasattr(Feedback, 'getListQuery') is True

def testFeedbackModelHasRestoreDefinition():
    assert hasattr(Feedback, 'restore') is True

def testFeedbackModelHasdestroyDefinition():
    assert hasattr(Feedback, 'destroy') is True

def testFeedbackModelHasisDeletedDefinition():
    assert hasattr(Feedback, 'isDeleted') is True

def testFeedbackModelHasgetFieldsDefinition():
    assert hasattr(Feedback, 'getFields') is True

def testFeedbackModelHasschemaDefinition():
    assert hasattr(Feedback, 'schema') is True

def testFeedbackModelHasgetDataTypeKeysDefinition():
    assert hasattr(Feedback, 'getDataTypeKeys') is True

def testFeedbackModelHasappendScopeDefinition():
    assert hasattr(Feedback, 'appendScope') is True

def testFeedbackModelHastypeRefDefinition():
    assert hasattr(Feedback, 'typeRef') is True

def testFeedbackModelHastypeCastDefinition():
    assert hasattr(Feedback, 'typeCast') is True

def testFeedbackModelHastoISODateDefinition():
    assert hasattr(Feedback, 'toISODate') is True

def testFeedbackModelHastoIntDefinition():
    assert hasattr(Feedback, 'toInt') is True