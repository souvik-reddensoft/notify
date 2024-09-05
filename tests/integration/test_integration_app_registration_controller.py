import os
import pytest
import mock
import json
from Application.roles.Models.Role import roles
from Core.Factories.Database import DbFactory as db
from tests.helper.auth import Auth
from tests.helper.createApp import createApp
from tests.helper.request import Request
from tests.helper.client import Client
from Application.app_registrations.Service_providers.CloudFlare import Cloudflare
from unittest.mock import MagicMock

BASE_URL = "app-registrations"
payload = {
    "app_slug": "hr"
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

@mock.patch.object(Cloudflare, 'findIfDnsExists', return_value = {'result': []})
@mock.patch.object(Cloudflare, 'addDns', return_value = {'success': True})
def testAppCreationInSetupApp(addDnsMock, findMock):
    app = createApp()
    with app.test_client() as client:
        token = Auth().login(client)
    req = Request(client, BASE_URL, roles, token, payload=payload).create(fetch_object_id_fn=print)
    assert req.data['status'] is True
    assert addDnsMock.called
    assert findMock.called

    # Test if app registration is actually created
    registration = db.instance['app_registrations'].find_one()
    assert registration['workspace'] == 'john-doe-test-corp-hr'


@mock.patch.object(Cloudflare, 'findIfDnsExists', return_value = {'result': []})
@mock.patch.object(Cloudflare, 'addDns', return_value = {'success': True})
def testAppListing(addDnsMock, findMock):
    # First setup the app
    app = createApp()
    with app.test_client() as client:
        token = Auth().login(client)
    req = Request(client, BASE_URL, roles, token, payload=payload).create(fetch_object_id_fn=print)
    assert req.data['status'] is True
    assert addDnsMock.called
    assert findMock.called

    # Test if app registration is actually created
    registration = db.instance['app_registrations'].find_one()
    assert registration['workspace'] == 'john-doe-test-corp-hr'

    #Retrieve the listing
    req = Request(client, BASE_URL, roles, token).list()
    assert len(req.data['data']['results']['results']['data']) == 1


@mock.patch.object(Cloudflare, 'findIfDnsExists', return_value = {'result': []})
@mock.patch.object(Cloudflare, 'addDns', return_value = {'success': True})
def testAppListingFiltered(addDnsMock, findMock):
    # Filter the listing
    app = createApp()
    with app.test_client() as client:
        token = Auth().login(client)
    req = Request(client, BASE_URL, roles, token, payload=payload).create(fetch_object_id_fn=print)
    assert req.data['status'] is True
    assert addDnsMock.called
    assert findMock.called

    # Test if app registration is actually created
    registration = db.instance['app_registrations'].find_one()
    assert registration['workspace'] == 'john-doe-test-corp-hr'

    # Update permissions to owner
    db.instance['user_permissions'].update_one({}, {
    "$push": { "permissions": "accounts~app-registrations~owner~list"}})
    db.instance['user_permissions'].update_one({}, {
    "$pull": { "permissions": "accounts~app-registrations~instance~list"}})

    db.instance['app_registrations'].insert_one({
        'workspace': 'test-hire',
        'org_id': registration['org_id']
    })

    #Retrieve the listing
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    request_client = Client(client)
    response = request_client["get"](f'{BASE_URL}/list', headers=headers)
    result = json.loads(response.data)
    assert len(result['data']['results']['results']['data']) == 1
    assert result['data']['results']['results']['data'][0]['workspace'] == 'john-doe-test-corp-hr'


@mock.patch.object(Cloudflare, 'findIfDnsExists', return_value = {'result': []})
@mock.patch.object(Cloudflare, 'addDns', return_value = {'success': True})
def testAppLock(addDnsMock, findMock):
    # First setup the app
    app = createApp()
    
    with app.test_client() as client:
        token = Auth().login(client)
    
    db.instance['roles'].insert_one({
        'app_slug': 'hr',
        'slug': 'account-owner-role',
        'name': 'Role that should not get inserted',
        'permissions': [
            'hr~module~scope~action',
            'hr~module1~scope1~action1'
        ]
    })
    req = Request(client, BASE_URL, roles, token, payload=payload).create(fetch_object_id_fn=print)
    assert req.data['status'] is True

    # Test if app registration is actually created
    registration = db.instance['app_registrations'].find_one()
    assert registration['workspace'] == 'john-doe-test-corp-hr'

    # Lock the app registration
    db.instance['app_registrations'].update_one({
        'workspace': 'john-doe-test-corp-hr'
    }, {
        '$set': {
            'lock': 1
        }
    })

    with app.test_client() as client1:
        fresh_signin_payload = {
            'email': Auth.email,
            'password': Auth.password,
            'host_data': {
                'fingerprint' : Auth.fingerprint
            }
        }
        headers = { 'Content-Type': 'application/json' }
        request_client = Client(client1)
        request_client["post"](f'/sign-in/', json=fresh_signin_payload, headers=headers)
        # result = json.loads(response.data)
    
    retrieved_permissions = db.instance['user_permissions'].find_one({})['permissions']
    count = 0
    for permission in retrieved_permissions:
        if permission.startswith('hr'):
            break
        count = count + 1

    assert len(retrieved_permissions) == count




    