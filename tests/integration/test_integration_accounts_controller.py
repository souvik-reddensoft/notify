import os
import pytest
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.accounts.Models.Accounts import accounts
from tests.helper.auth import auth

BASE_URL = "accounts"

@pytest.fixture(scope="session", autouse=True)
def myFixture():
    os.environ["FLASK_ENV"] = "test"
    yield

# @pytest.fixture(autouse=True)
# def runAroundTests():
#     yield
#     accounts.getCollection().delete_many({})

def testListReturns200ResponseCode():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, accounts, token).list()
        assert req.status_code == 200

def testActiveUserCountReturns200ResponseCode():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, accounts, token).custom("activeusers")
        assert req.status_code == 200

def testActiveUserCountReturnsCountAsInt():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, accounts, token).custom("activeusers")
        assert type(req.data["data"]["count"]) == int
        assert req.data["data"]["count"] == 1

def testOverviewReturns200ResponseCode():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, accounts, token).custom("overview")
        assert req.status_code == 200

def testOverviewReturnsSuccessMessage():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        req = Request(client, BASE_URL, accounts, token).custom("overview")
        assert req.data["message"] == "Accounts fetched successfully"