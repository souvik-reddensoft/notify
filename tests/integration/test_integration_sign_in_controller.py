import os
import json
import pytest
from bson.objectid import ObjectId
from tests.helper.createApp import createApp
from tests.helper.request import Request
from Application.signup.Models.Signup import signup
from Application.signin.Models.Jwt import jwt
from Application.users.Models.Users import users
from Application.accounts.Models.Accounts import accounts
from Core.Factories.Database import DbFactory as db
from tests.helper.auth import auth

BASE_URL = "sign-in"
access_token = "ya29.a0AX9GBdUunz5R0sOZ-6ScCT_F2HIc5aPYQI7ew7WtBKXITXZ9NwEb-PS70RDfUUNwf3QjFUGMt73Szg_go5EJOzSlM4DoGDWACqXyXVc3oKcUbxvE7PnWaq2HViZ_o9jVd93UW8_iMPoF763bCiDeB0IWcNJRQAaCgYKAW8SARISFQHUCsbC_dKHwTQDuhOwbnMa6CVgHg0165"

payload = {
    "token": access_token,
    "host_data": {
        "fingerprint": "asdajsdhasd76atsdasd"
    }
}

def googleSignup(client):
    data = {
        "token": access_token,
    }
    # Request(client, "sign-up", signup).custom("", http_method="post", payload=data)
    resp = client.post('/sign-up/', json=data, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        raise Exception("Registration failed")

def signUP(client, email = None, password = None):
    data = {
        "first_name": "John",
        "company_name": "John Doe Test Corp.",
        "last_name": "Doe",
        "email" : email or "ritwik.math@codeclouds.com",
        "password" : password or "Test@123",
    }
    resp = client.post('/sign-up/', json=data, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        raise Exception("Registration failed")
    return json.loads(resp.data)

def signIn(client, email = None, password = None):
    data = {
        "email" : email or "ritwik.math@codeclouds.com",
        "password" : password or "Test@123",
        "host_data": {
            "fingerprint": "9e8ce2a57b80b51f3b64c0ac64eb324c2"
        }
    }
    resp = client.post('/sign-in/', json=data, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        raise Exception("Login failed")
    data = json.loads(resp.data)
    return data['result']['access_token']

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

# def testSignInReturns200ResponseCode():
#     app = createApp()
#     with app.test_client() as client:
#         googleSignup(client)
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         print(req.data)
#         assert req.status_code == 200

# def testSignInReturnsAccessToken():
#     app = createApp()
#     with app.test_client() as client:
#         googleSignup(client)
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         assert req.status_code == 200
#         assert isinstance(req.data.get("result", {}).get("access_token", {}), str)

# def testSignInReturnsRefreshToken():
#     app = createApp()
#     with app.test_client() as client:
#         googleSignup(client)
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         assert req.status_code == 200
#         assert isinstance(req.data.get("result", {}).get("refresh_token", {}), str)

# def testSignInReturnsPasswordMismatchIfGoogleAccountTryToLoginConventionally():
#     app = createApp()
#     with app.test_client() as client:
#         googleSignup(client)
#         payload = {
#             "email": "ritwik.math@codeclouds.com",
#             "password": "Test@1234",
#             "host_data": {
#                 "fingerprint": "macpostman3-new"
#             }
#         }
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         assert req.status_code == 422
#         assert req.data.get("success", True) is False
#         assert req.data.get("message", "") == "Wrong password. You have 4 attempts remaining"

# def testSignInThrowsErrorIfUserNotExists():
#     app = createApp()
#     with app.test_client() as client:
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         assert req.status_code == 422
#         assert req.data.get("success") is False
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         assert req.status_code == 422
#         assert req.data.get("success") is False

# def testSigninWithGoogleAfterConventionalSignup():
#     app = createApp()
#     with app.test_client() as client:
#         result = signUP(client)
#         users.update(ObjectId(result.get("data", {}).get("insertedIds", {}).get("user")), None, {
#             "status": 1
#         })
#         accounts.update(ObjectId(result.get("data", {}).get("insertedIds", {}).get("account")), None, {
#             "status": 1
#         })
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         assert req.status_code == 200
#         assert req.data.get("success", True) is True

# def testSigninWithGoogleVerifiesUnverifiedAccountAndUser():
#     app = createApp()
#     with app.test_client() as client:
#         result = signUP(client)
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         print(req.data)
#         assert req.status_code == 200
#         assert req.data.get("success", True) is True
#         user = users.findOne({
#             "_id": ObjectId(result.get("data", {}).get("insertedIds", {}).get("user"))
#         })
#         account = accounts.find(ObjectId(result.get("data", {}).get("insertedIds", {}).get("account")))
#         assert user.get("status") == 1
#         assert account.get("status") == 1

# def testSigninWithGoogleVerifiesInvitedUser():
#     app = createApp()
#     with app.test_client() as client:
#         token = auth.login(client)
#         auth.token = ""
#         db.instance.roles.insert_one({
#                 "_id": ObjectId("6358df9447e7b1826ad82de3"),
#                 "slug": "developer-role",
#                 "app_slug": "accounts",
#                 "permissions": [
#                     "accounts~users~all~change-password"
#                 ],
#                 "name": "Developer",
#                 "type": [
#                     1, 2
#                 ]
#             })
#         invite_data = {
#             "first_name": "Ritwik",
#             "last_name": "Math",
#             "email": "ritwik.math@codeclouds.com",
#             "role_ids": [
#                 "6358df9447e7b1826ad82de3"
#             ]
#         }
#         req = Request(client, "users", users, token=token).custom(url="invite", http_method="post", payload=invite_data)
#         assert req.status_code == 200
#         assert req.data.get("success", True) is True
#         req = Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
#         user = users.findOne({
#             "email": "ritwik.math@codeclouds.com"
#         })
#         assert user.get("status") == 1

def testSinginAsClientReturnsJWTToken():
    app = createApp()
    with app.test_client() as client:
        token = auth.login(client)
        db.instance.roles.insert_one({
                "_id": ObjectId("6358df9447e7b1826ad82de3"),
                "slug": "developer-role",
                "app_slug": "accounts",
                "permissions": [
                    "accounts~users~all~change-password"
                ],
                "name": "Developer",
                "type": [
                    1, 2
                ]
            })
        invite_data = {
            "first_name": "Ritwik",
            "last_name": "Math",
            "email": "ritwik.math@codeclouds.com",
            "role_ids": [
                "6358df9447e7b1826ad82de3"
            ]
        }
        invite_req = Request(client, "users", users, token=token).custom(url="invite", http_method="post", payload=invite_data)
        Request(client, BASE_URL, jwt).custom(http_method="post", payload=payload)
        data = {
            "user_id": invite_req.data.get("data")[0]
        }
        sac_req = Request(client, "sign-in", users, token=token).custom(url="signin-as-client", http_method="post", payload=data)
        assert sac_req.status_code == 200
        assert "impersonated_token" in sac_req.data.get("data")
        assert isinstance(sac_req.data.get("data").get("impersonated_token").get("access_token"), str)