import os
import pytest
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.feedback.Models.Feedback import feedback
from tests.helper.auth import auth

BASE_URL = "feedbacks"
payload = {
    "feedback":"test feedback",
    "rate":3,
    "attachment":["attachment1","attachment2"],
    "app_slug":"hr~commerce"
}

def getErrorData(data):
    return data

@pytest.fixture(scope="session", autouse=True)
def myFixture():
    os.environ["FLASK_ENV"] = "test"
    yield

def testListReturns200ResponseCode():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, feedback, token).list()
        assert req.status_code == 200

def testCreateReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, feedback, token, payload=payload).create()
    assert req.data["message"] == "Feedback created successfully"

def testCreateReturns400ResponseOnRateGreaterThan10():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    payload = {
        "feedback":"test feedback",
        "rate":20,
        "attachment":["attachment1","attachment2"],
        "app_slug":"hr~commerce"
    }
    req = Request(client, BASE_URL, feedback, token, payload=payload).create(fetch_object_id_fn=getErrorData)
    assert req.status_code == 400
    assert req.data['message']['rate'][0] == 'max value is 10'

def testCreateReturns400ResponseOnFeedbackEmpty():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    payload = {
        "feedback":"",
        "rate":3,
        "attachment":["attachment1","attachment2"],
        "app_slug":"hr~commerce"
    }
    req = Request(client, BASE_URL, feedback, token, payload=payload).create(fetch_object_id_fn=getErrorData)
    assert req.status_code == 400
    assert req.data['message']['feedback'][0] == 'empty values not allowed'