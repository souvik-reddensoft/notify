import os
import pytest
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.user_permissions.Models.UserPermissions import user_permissions
from tests.helper.auth import auth

BASE_URL = "permissions"
payload = {
    "permission_key":"permit_NjNhYzM5MmI4MWYzOTk2NjQwZDBjNWVi_NjNhYzM5MmE4MWYzOTk2NjQwZDBjNWU5",
    "permissions":{"permission":"accounts~feedbacks~all~create"}
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
        req = Request(client, BASE_URL, user_permissions, token, payload=payload).create()
        print(req.data)
        assert req.status_code == 200

def testListReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, user_permissions, token, payload=payload).list()
        assert req.status_code == 200
