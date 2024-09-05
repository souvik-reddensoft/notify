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

# def testLoginShouldFailOnLockedWorkspace(accessToken):
#     app = createApp()
#     # Signin should fail if app has billing lock
#     organization = db.instance['organizations'].find_one({})
#     db.instance['app_registrations'].insert_one({
#         "workspace" : 'test-workspace-hr',
#         'app_slug': 'hr',
#         'org_id': organization['_id'],
#         'lock': 1
#     })

#     headers = {"Content-Type": "application/json"}
#     with app.test_client() as client:
#         request_client = Client(client)
#         payload = {
#             "email": Auth.email,
#             "password": Auth.password,
#             "workspace": "test-workspace-hr.pypa.com",
#             "host_data": {
#                 "fingerprint": Auth.fingerprint
#             }
#         }
#         response = request_client['post']('/sign-in/', json=payload, headers=headers)
#         assert response.status_code == 422

def testAccountDeactivatesCorrectly(accessToken):
    user = {
        'first_name': 'Test',
        'last_name': 'Name',
        'middle_name': 'Middle',
        'email': 'test@another.com',
        'password': 'password',
        'company_name': 'Another',
        'company_country': 'INDIA'
    }
    headers = {"Content-Type": "application/json"}
    app = createApp()
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client['post']('/sign-up/', json=user, headers=headers)
        account_id = json.loads(response.data)['data']['insertedIds']['account']
        payload = {
            'ids': [],
            'action': 'deactivate'
        }
        headers['Authorization'] = f'Bearer {accessToken}'
        response = request_client['post']('/accounts/manage-status', json=payload, headers=headers)
        print(response.data)
        assert response.status_code == 200
        account = db.instance['accounts'].find_one({"_id":ObjectId(account_id)})
        assert account.get('deactivate',{}).get('deactivated_at') is not None
        assert 5 in account.get('status_stack',[])
        assert account['status'] == 5
