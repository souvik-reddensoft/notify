import os
import pytest
from bson.objectid import ObjectId
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.signup.Models.Signup import signup
from Core.Factories.Database import DbFactory as db

BASE_URL = "sign-up"
access_token = "ya29.a0AX9GBdWmSL_IFMz0C00lOvalntQiBb94eTWdS_TZO3r-y7QFiJDH0AuzzpXKL7aBRJs-3X9ySguwdOrjAG67fGwFtY2GG9V0Xq5vEJLG28T8bgMkFr-GY9FarIAzM5OOJgeHHxTAneFNX1FIoXbAPYWaTJdg5AaCgYKAR4SARISFQHUCsbC7rEB07yEHtJpL_onE0df2A0165"

payload = {
    "token": access_token,
}

@pytest.fixture(scope="session", autouse=True)
def myFixture():
    os.environ["FLASK_ENV"] = "test"
    yield

@pytest.fixture(autouse=True)
def runAroundTests():
    createApp()
    for col in db.instance.list_collection_names():
        db.instance[col].drop()
    yield

def testSignUpReturns200ResponseCode():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        print(req.data)
        assert req.status_code == 200

def testGoogleSignUpCreateUserWithoutPassword():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        user = db.instance.users.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["user"]) 
        })
        assert user.get("password") is None 
        assert req.status_code == 200

def testGoogleSignUpCreateUserWithoutPassword():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        user = db.instance.users.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["user"]) 
        })
        assert user.get("password") is None
        assert req.status_code == 200

def testGoogleSignUpCreateUserWithoutVerification():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        assert req.status_code == 200
        user = db.instance.users.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["user"]) 
        })
        assert 'invitation' not in user

def testGoogleSignUpCreateCompanyNameWithEmailDomain():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        assert req.status_code == 200
        user = db.instance.users.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["user"]) 
        })
        account = db.instance.accounts.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["account"]) 
        })
        assert account.get("company_name") == user.get("email").split("@")[1]

def testGoogleSignUpCreateUserWithGoogleSignupTrue():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        assert req.status_code == 200
        user = db.instance.users.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["user"]) 
        })
        assert user.get("google_sign_up")is True

def testGoogleSignUpCreateUserWithStatusOne():
    app = createApp()
    with app.test_client() as client:
        req = Request(client, BASE_URL, signup).custom("", http_method="post", payload=payload)
        assert req.status_code == 200
        user = db.instance.users.find_one({
            "_id": ObjectId(req.data["data"]["insertedIds"]["user"]) 
        })
        assert user.get("status") == 1