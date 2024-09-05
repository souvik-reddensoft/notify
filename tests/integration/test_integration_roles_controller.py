import os
import pytest
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.roles.Models.Role import roles
from tests.helper.auth import auth

BASE_URL = "roles"
payload = {
    "name" : "Developer",
	"description" : "It is developer role",
	"app_slug" : "accounts",
	"company_id" : "63890193ef9cb35bbf0358ba",
	"permissions" : ["users.developer.view", "users.developer.create"]
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
        req = Request(client, BASE_URL, roles, token).list()
        assert req.status_code == 200

def testCreateReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, roles, token, payload=payload).create()
    assert req.status_code == 200

def testUpdateReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, roles, token, payload=payload).create().update({'name':'Tester'})
    assert req.status_code == 200

def testgetPermissionsReturnsSuccessfulResponse():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
    req = Request(client, BASE_URL, roles, token, payload=payload).custom(url='permission/accounts/default_roles_for_external_owners', http_method='get')
    assert req.status_code == 200