from flask import Flask, request
import json
from unittest.mock import MagicMock
import mock # pylint:disable=E0401
from Core.Controllers.Controller import Controller
from Application.feedback.Controllers.Feedback import feedback, Feedback as FeedbackClass
from Application.feedback.Models.Feedback import Feedback

app = Flask(__name__)

def testFeedbackControllerExtendsBaseController():
    assert issubclass(FeedbackClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfFeedbacksModel():
    assert isinstance(feedback.model, Feedback) is True

def testFeedbackControllerHasListMethod():
    assert hasattr(FeedbackClass, 'list') is True

def testFeedbackControllerHasCreateMethod():
    assert hasattr(FeedbackClass, 'create') is True

def testFeedbackControllerHasUpdateMethod():
    assert hasattr(FeedbackClass, 'update') is True

def testFeedbackControllerHasDeleteMethod():
    assert hasattr(FeedbackClass, 'delete') is True

def testFeedbackControllerHasDestroyMethod():
    assert hasattr(FeedbackClass, 'destroy') is True

def testFeedbackControllerHasViewMethod():
    assert hasattr(FeedbackClass, 'view') is True

def testFeedbackControllerHasTrashMethod():
    assert hasattr(FeedbackClass, 'trash') is True

def testFeedbackControllerHasRestoreMethod():
    assert hasattr(FeedbackClass, 'restore') is True

@mock.patch.object(Feedback, 'list')
def testFeedbackModelListIsCalledInFeedbackControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        feedback.list()
        assert Feedback().list.called # pylint: disable=E1101

@mock.patch.object(Feedback, 'create')
def testFeedbackModelCreateIsCalledInFeedbackControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        feedback.validate = _mock
        feedback.create()
        assert feedback.validate.called # pylint: disable=E1101
        assert Feedback().create.called # pylint: disable=E1101

@mock.patch.object(Feedback, 'isDeleted', return_value = None)
@mock.patch.object(Feedback, 'update')
def testFeedbackModelUpdateIsCalledInFeedbackControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        feedback.validate = _mock
        feedback.update('1234')
        assert Feedback().isDeleted.called # pylint: disable=E1101
        assert feedback.validate.called # pylint: disable=E1101
        assert Feedback().update.called # pylint: disable=E1101

@mock.patch.object(Feedback, 'isDeleted', return_value = None)
@mock.patch.object(Feedback, 'delete')
def testFeedbackModelDeleteIsCalledInFeedbackControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        feedback.delete('1234')
        assert Feedback().isDeleted.called # pylint: disable=E1101
        assert Feedback().delete.called # pylint: disable=E1101

@mock.patch.object(Feedback, 'isDeleted', return_value = {})
@mock.patch.object(Feedback, 'restore')
def testFeedbackModelRestoreIsCalledInFeedbackControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        feedback.restore('1234')
        assert Feedback().isDeleted.called # pylint: disable=E1101
        assert Feedback().restore.called # pylint: disable=E1101

@mock.patch.object(Feedback, 'find', return_value = {})
@mock.patch.object(Feedback, 'destroy', return_value = 1)
def testFeedbackModelDestroyIsCalledInFeedbackControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        feedback.destroy('1234')
        assert Feedback().find.called # pylint: disable=E1101
        assert Feedback().destroy.called # pylint: disable=E1101
