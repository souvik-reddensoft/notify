import os
import pytest
import mock
from Core.Factories.Database import DbFactory as db
from tests.helper.auth import Auth
from tests.helper.createApp import createApp
from Application.user_permissions.Helpers import Helper as PermissionsHelper
from tests.helper.client import Client
import json

BASE_URL = "sign-in"


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

def testPermissionRegenerationOnRefreshToken():
    app = createApp()
    with app.test_client() as client:
        auth = Auth()
        token = auth.login(client)
        refresh = auth.refresh_token

    db.instance['user_permissions'].delete_many({})
    payload = {
        'refresh_token': refresh
    }
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["post"](f'{BASE_URL}/refresh', json=payload, headers=headers)
        assert response.status_code == 200

        # Now check if the permissions are getting regenerated as expected
        permissions = db.instance['user_permissions'].find_one({})
        assert permissions is not None
        assert len(permissions['permissions']) > 0


# @mock.patch.object(PermissionsHelper, 'recreatePermissions')
def testPermissionRegenerationOnSwitch():
    app = createApp()
    with app.test_client() as client:
        token = Auth().login(client)
    organization = db.instance['organizations'].find_one({})
    assert organization is not None
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/switch/{str(organization["_id"])}', headers=headers)
        assert response.status_code == 200

        # Now check if the permissions are getting regenerated as expected
        permissions = db.instance['user_permissions'].find_one({})
        assert permissions is not None
        assert len(permissions['permissions']) > 0




    