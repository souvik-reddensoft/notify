import os
import pytest
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.scopes.Models.Scope import scope
from tests.helper.auth import auth

BASE_URL = "scopes"
payload = {
    "name":"scope1",
    "slug":"scope_1",
    "description":"scope description",
    "app_slug":"accounts"
}

def getErrorData(data):
    return data

@pytest.fixture(scope="session", autouse=True)
def myFixture():
    os.environ["FLASK_ENV"] = "test"
    yield

def testCreateReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, scope, token, payload=payload).create()
    assert req.status_code == 200

def testListReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, scope, token, payload=payload).list()
    assert req.status_code == 200

def testUpdateReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, scope, token, payload=payload).create().update({"description":"revised description"})
    assert req.status_code == 200
