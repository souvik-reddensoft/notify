import os
import pytest
import mock
from Core.Factories.Database import DbFactory as db
from tests.helper.auth import Auth
from tests.helper.createApp import createApp
from Application.user_permissions.Helpers import Helper as PermissionsHelper
from tests.helper.client import Client
import json
from bson.objectid import ObjectId

BASE_URL = "roles"

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


def testRoleListing(accessToken):
    # Role listing should show 2 users since one user has two roles
    app = createApp()
    organization = db.instance['organizations'].find_one({})
    roles_doc = [
        {   
            '_id': ObjectId('634d28ab7c2b218391a183ea'),
           'slug': 'role-1',
           'name': "Role 1",
          'app_slug' : 'accounts',
          'permissions': ['asdasd', 'asdasd'],
          'org_id': organization['_id']
        },
        {
           '_id': ObjectId('634d28ab7c2b218391a183eb'),
           'slug': 'role-2',
           'name': "Role 2",
          'app_slug' : 'accounts',
          'permissions': ['asdasd', 'asdasd'],
          'org_id': organization['_id']
        }
    ]
    db.instance['roles'].insert_many(roles_doc)
     #assign these roles to the user
    db.instance['users'].update_one({ 'organizations.id': organization['_id']  }, {
        # '$set': {
            '$addToSet': {
                'organizations.$.accounts.role_ids': {
                    '$each': [ObjectId('634d28ab7c2b218391a183ea'), ObjectId('634d28ab7c2b218391a183eb')]
                 }
            }
        # }
    })
    
    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/list', headers=headers)
        result = json.loads(response.data)

        assert len(result['data']['results']['results']['data']) == len(roles_doc)
        assert result['data']['results']['results']['data'][0]['user_count'] == 1
        assert result['data']['results']['results']['data'][1]['user_count'] == 1



def testRoleListingWithOneRole(accessToken):
    # Role listing should show 1 users since one user has one role
    app = createApp()
    organization = db.instance['organizations'].find_one({})
    roles_doc = [
        {   
            '_id': ObjectId('634d28ab7c2b218391a183ea'),
           'slug': 'role-1',
           'name': "Role 1",
          'app_slug' : 'accounts',
          'permissions': ['asdasd', 'asdasd'],
          'org_id': organization['_id']
        },
        {
           '_id': ObjectId('634d28ab7c2b218391a183eb'),
           'slug': 'role-2',
           'name': "Role 2",
          'app_slug' : 'accounts',
          'permissions': ['asdasd', 'asdasd'],
          'org_id': organization['_id']
        }
    ]
    db.instance['roles'].insert_many(roles_doc)
     #assign these roles to the user
    db.instance['users'].update_one({ 'organizations.id': organization['_id']  }, {
        # '$set': {
            '$addToSet': {
                'organizations.$.accounts.role_ids': {
                    '$each': [ObjectId('634d28ab7c2b218391a183ea')]
                 }
            }
        # }
    })
    
    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/list', headers=headers)
        result = json.loads(response.data)

        assert len(result['data']['results']['results']['data']) == len(roles_doc)
        assert result['data']['results']['results']['data'][0]['user_count'] == 1
        assert 'user_count' not in result['data']['results']['results']['data'][1]



