import json
import os

import mock
import pytest

from Application.user_permissions.Helpers import Helper as PermissionsHelper
from Core.Factories.Database import DbFactory as db
from tests.helper.auth import Auth
from tests.helper.client import Client
from tests.helper.createApp import createApp
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import base64

BASE_URL = "sign-in"

#-------------------- Common portion for all tests ---------------------------------
@pytest.fixture(scope="session", autouse=True)
def myFixture():
    os.environ["FLASK_ENV"] = "test"
    yield

@pytest.fixture(autouse=True)
def runAroundTests():
    app = createApp()
    for col in db.instance.list_collection_names():
        db.instance[col].drop()
    yield app

@pytest.fixture()
def accessToken(runAroundTests):
    with runAroundTests.test_client() as client:
        token = Auth().login(client)
    return token
#-------------------- Common portion for all tests ---------------------------------

def testLoginShouldFailOnLockedWorkspace(accessToken):
    app = createApp()
    # Signin should fail if app has billing lock
    organization = db.instance['organizations'].find_one({})
    db.instance['app_registrations'].insert_one({
        "workspace" : 'test-workspace-hr',
        'app_slug': 'hr',
        'org_id': organization['_id'],
        'lock': 1
    })

    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        payload = {
            "email": Auth.email,
            "password": Auth.password,
            "workspace": "test-workspace-hr.pypa.com",
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert response.status_code == 422


def testLoginShouldFailOnLockedWorkspaceOfUser(accessToken):
    app = createApp()
    # Signin should fail if app has billing lock
    organization = db.instance['organizations'].find_one({})
    db.instance['app_registrations'].insert_one({
        "workspace" : 'test-workspace-hr',
        'app_slug': 'hr',
        'org_id': organization['_id'],
    })

    db.instance['users'].update_one({'organizations.id': organization['_id']}, {
        '$set': {'organizations.$.hr': {
            'lock': {
                'locked_at': datetime.now()
            }
        }}
    })

    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        payload = {
            "email": Auth.email,
            "password": Auth.password,
            "workspace": "test-workspace-hr.pypa.com",
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert response.status_code == 422


def testLoginShouldFailOnWrongPasswordEntry(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        payload = {
            "email": Auth.email,
            "password": "thisiswrongpassword",
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert response.status_code == 422
        assert json.loads(response.data)['success'] is False


def testMultipleWrongPasswordAttemptShouldLockTheUserTemporarily(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        payload = {
            "email": Auth.email,
            "password": "thisiswrongpassword",
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        for i in range(5):
            request_client['post']('/sign-in/', json=payload, headers=headers)
            user = db.instance['users'].find_one({'email': Auth.email})
            user['lock']['wrong_attempt'] = i+1
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert response.status_code == 422
        data = json.loads(response.data)
        user = db.instance['users'].find_one({'email': Auth.email})
        assert user['lock']['wrong_attempt'] is None
        assert user['lock']['status'] == 'temp-lock'
        assert 3 in user['status_stack']
        assert user['status'] == 3
        assert data['success'] is False


def testUserCanNotLogInWithCorrectCredsAfterBeingLockedForMultipleWrongAttempts(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        payload = {
            "email": Auth.email,
            "password": "thisiswrongpassword",
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        for _ in range(5):
            request_client['post']('/sign-in/', json=payload, headers=headers)
        payload['password'] = Auth.password
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert response.status_code == 422
        assert json.loads(response.data)['success'] is False


def testUserCanLoginBackAfter24HoursAfterBeingTemporarilyLocked(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        payload = {
            "email": Auth.email,
            "password": "thisiswrongpassword",
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        for _ in range(5):
            request_client['post']('/sign-in/', json=payload, headers=headers)
        time = db.instance['users'].find_one({'email': Auth.email})['lock']['last_wrong_attempt_at']
        new_time = time - timedelta(hours=24)
        db.instance['users'].find_one_and_update({'email': Auth.email},{'$set':{
            'lock.last_wrong_attempt_at': new_time
        }})
        payload['password'] = Auth.password
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert response.status_code == 200
        user = db.instance['users'].find_one({'email': Auth.email})
        assert user['status'] == 1
        assert 3 not in user['status_stack']
        assert user['lock']['status'] is None


def testUserCanNotLoginAfterBeingLockedBySaasAdminForCustomDuration(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        db.instance['users'].find_one_and_update({
            'email': Auth.email
        }, {
            '$set':{
                'lock.lock_time': datetime.now() + timedelta(minutes=5),
                'lock.status': "admin-lock"
            }
        })
        payload = {
            "email": Auth.email,
            "password": Auth.password,
            "host_data": {
                "fingerprint": Auth.fingerprint
            }
        }
        response = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert json.loads(response.data)['success'] is False
        assert response.status_code == 422


def testUserStatusStackIsBeingMaintainedOnMultipleActions(accessToken):
    app = createApp()
    admin = {
        'first_name': 'Saas',
        'last_name': 'Admin',
        'middle_name': 'Middle',
        'email': 'admin@saas.com',
        'password': 'iamadmin',
        'company_name': 'Saas',
        'company_country': 'INDIA'
    }
    role = db.instance['roles'].insert_many([{
        "slug": 'account-saas-role',
        "app_slug": "accounts",
        "name": "Saas Role",
        "permissions": [
            'accounts~users~all~manage-status',
            'accounts~users~all~manage-lock'
        ]
        },{
      "slug": 'account-owner-role',
      "app_slug": "accounts",
      "name": "Accounts Role"
    }])

    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=admin, headers=headers)
        org_id = json.loads(res.data)['data']['insertedIds']['organization']
        db.instance['users'].update_one({'email': admin['email'], 'organizations.id': ObjectId(org_id)}, {'$set':{
            'organizations.$.accounts.role_ids':[ObjectId(_id) for _id in role.inserted_ids]
        }})
        user = db.instance['users'].find_one({'email': Auth.email})
        lock_payload = {
            "ids": [str(user['_id'])],
            "lock_action":"lock",
            "locked_indefinite": False,
            "lock_duration": 1,
            "lock_type": 'hours'
        }
        deactivate_payload = {
            "ids": [str(user['_id'])],
            "action": "deactivate",
            "app": "hr"
        }
        admin_payload = {
            'email': admin['email'],
            'password': admin['password'],
            'host_data': {
                'fingerprint': 'Demo'
            }
        }
        admin = db.instance['users'].find_one({'email': admin['email']})
        request_client['get'](f"/users/verify-email/{admin['organizations'][0]['invitation']['hash']}")
        token_data = request_client['post']('/sign-in/', json=admin_payload, headers=headers)
        headers['Authorization'] = f"Bearer {json.loads(token_data.data)['result']['access_token']}"
        # checking if the user has been locked
        lock_response = request_client['post']('/users/manage-lock', json=lock_payload, headers=headers)
        assert lock_response.status_code == 200
        # checking if the user has been deactivated
        deactivate_response = request_client['post']('/users/manage-status', json=deactivate_payload, headers=headers)
        assert deactivate_response.status_code == 200
        assert json.loads(deactivate_response.data)['success'] is True
        # checking if the status stack is maintaining its order of action
        modified_user = db.instance['users'].find_one({'email':Auth.email})
        assert modified_user['status_stack'][0] == 3
        assert modified_user['status_stack'][1] == 5
        assert modified_user['status'] == 5


def testThrowsErrorAtSigninWhenUserIsLocked(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    user = db.instance['users'].find_one({'email':Auth.email})
    db.instance['users'].update_one({'email':Auth.email, 'organizations.id': ObjectId(user['organizations'][0]['id'])},{'$set':{'organizations.$.lock.status': "admin-lock"}})
    payload = {
        'email': Auth.email,
        'password': Auth.password,
        'host_data': {
            'fingerprint': Auth.fingerprint
        }
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-in/', json=payload, headers=headers)
        assert res.status_code == 422


def testUserGetsErrorAtTokenRefreshIfThePersonIsLockedForTheOrg(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    payload = {
        'email': Auth.email,
        'password': Auth.password,
        'host_data': {
            'fingerprint': Auth.fingerprint
        }
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-in/', json=payload, headers=headers)
        decoded_id = json.loads(res.data)['result']['active_company'].encode('ascii')
        decoded_id = base64.b64decode(decoded_id).decode('ascii')
        headers['Authorization'] = f"Bearer {json.loads(res.data)['result']['access_token']}"
        db.instance['users'].update_one({'email':Auth.email, 'organizations.id': ObjectId(decoded_id)},{'$set':{'organizations.$.lock.status': "admin-lock"}})
        response = request_client['post']('/sign-in/refresh', json={'refresh_token':json.loads(res.data)['result']['refresh_token']}, headers=headers)
        assert response.status_code == 422
        assert json.loads(response.data)['success'] is False


def testUserGetsErrorAtTokenRefreshIfThePersonIsDeactivatedForTheOrg(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    payload = {
        'email': Auth.email,
        'password': Auth.password,
        'host_data': {
            'fingerprint': Auth.fingerprint
        }
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-in/', json=payload, headers=headers)
        decoded_id = json.loads(res.data)['result']['active_company'].encode('ascii')
        decoded_id = base64.b64decode(decoded_id).decode('ascii')
        headers['Authorization'] = f"Bearer {json.loads(res.data)['result']['access_token']}"
        db.instance['users'].update_one({'email':Auth.email, 'organizations.id': ObjectId(decoded_id)},{'$set':{'organizations.$.deactivate.status': "deactivated", 'organizations.$.deactivate.deactivated_at': datetime.now()}})
        response = request_client['post']('/sign-in/refresh', json={'refresh_token':json.loads(res.data)['result']['refresh_token']}, headers=headers)
        assert response.status_code == 422
        assert json.loads(response.data)['success'] is False


def testUserGetsErrorAtSwitchIfThePersonIsLockedForTheOrg(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    payload = {
        'email': Auth.email,
        'password': Auth.password,
        'host_data': {
            'fingerprint': Auth.fingerprint
        }
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-in/', json=payload, headers=headers)
        decoded_id = json.loads(res.data)['result']['active_company'].encode('ascii')
        decoded_id = base64.b64decode(decoded_id).decode('ascii')
        headers['Authorization'] = f"Bearer {json.loads(res.data)['result']['access_token']}"
        db.instance['users'].update_one({'email':Auth.email, 'organizations.id': ObjectId(decoded_id)},{'$set':{'organizations.$.lock.status': "admin-lock"}})
        response = request_client['get'](f"/sign-in/switch/{decoded_id}", json={}, headers=headers)
        assert response.status_code == 422
        assert json.loads(response.data)['success'] is False


def testUserGetsErrorAtSwitchIfThePersonIsDeactivatedForTheOrg(accessToken):
    app = createApp()
    headers = {"Content-Type": "application/json"}
    payload = {
        'email': Auth.email,
        'password': Auth.password,
        'host_data': {
            'fingerprint': Auth.fingerprint
        }
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-in/', json=payload, headers=headers)
        decoded_id = json.loads(res.data)['result']['active_company'].encode('ascii')
        decoded_id = base64.b64decode(decoded_id).decode('ascii')
        headers['Authorization'] = f"Bearer {json.loads(res.data)['result']['access_token']}"
        db.instance['users'].update_one({'email':Auth.email, 'organizations.id': ObjectId(decoded_id)},{'$set':{'organizations.$.deactivate.status': "deactivated", 'organizations.$.deactivate.deactvated_at': datetime.now()}})
        response = request_client['get'](f"/sign-in/switch/{decoded_id}", json={}, headers=headers)
        assert response.status_code == 422
        assert json.loads(response.data)['success'] is False
        