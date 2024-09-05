import json
import os
import pprint
import mock
import pytest

from Application.user_permissions.Helpers import Helper as PermissionsHelper
from Core.Factories.Database import DbFactory as db
from tests.helper.auth import Auth
from tests.helper.client import Client
from tests.helper.createApp import createApp
from datetime import datetime, timedelta
from bson.objectid import ObjectId

BASE_URL = "users"
#-------------------- Common portion for all tests ---------------------------------
@pytest.fixture(scope="session", autouse=True)
def myFixture():
    os.environ["FLASK_ENV"] = "test"
    yield

@pytest.fixture(autouse=True)
def runAroundTests():
    app = createApp()
    print("============================++++++++++++++========================")
    for col in db.instance.list_collection_names():
        db.instance[col].drop()
    return app

@pytest.fixture()
def accessToken(runAroundTests):
    with runAroundTests.test_client() as client:
        token = Auth().login(client)
    return token
#-------------------- Common portion for all tests ---------------------------------

def testGetUserProfile(accessToken):
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/profile', headers=headers)
        result = json.loads(response.data)
        assert response.status_code == 200
        assert result['data'] is not None
        assert result['data']['user']['email'] is not None
        assert len(result['data']['organizations'][0]['roles']) > 0 

def testShouldShowNonDeactivatedOrganizations(accessToken):
    # Should show all organizations as none are deactivated
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        assert len(result['data']) == 1
        assert len(result['data'][0]['organizations']) == 1
        assert result['data'][0]['organizations'][0]['name'] == Auth.organization_name

def testFilterOutDeactivatedOrganizations(accessToken):
    # Should filter out deactivated organizations
    result = db.instance['organizations'].insert_one({
        'name': 'Deactivated Company'
    })
    db.instance['users'].update_one({}, {
        '$push': {
            'organizations': {
                'id': result.inserted_id,
                'role_ids': [],
                'deactivate': { 'deactivated_at': datetime.now() }
            }
        }
    })
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        assert len(result['data']) == 1
        assert len(result['data'][0]['organizations']) == 1
        assert result['data'][0]['organizations'][0]['name'] == Auth.organization_name


def testUsersGetsDeactivatedWithUserIds(accessToken):
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
            'accounts~users~all~manage-status'
        ]
        },{
        "slug": 'account-owner-role',
        "app_slug": "accounts",
        "name": "Accounts Role"
    }])
    headers = {"Content-Type": "application/json"}
    app = createApp()
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=admin, headers=headers)
        org_id = json.loads(res.data)['data']['insertedIds']['organization']
        db.instance['users'].update_one({'email': admin['email'], 'organizations.id': ObjectId(org_id)}, {'$set':{
            'organizations.$.accounts.role_ids':[ObjectId(_id) for _id in role.inserted_ids]
        }})
        user = db.instance['users'].find_one({'email': Auth.email})
        deactivate_payload = {
            "ids": [str(user['_id'])],
            "action": "deactivate"
        }
        admin_payload = {
            'email': admin['email'],
            'password': admin['password'],
            'host_data': {
                'fingerprint': 'Demo'
            }
        }
        db.instance['users'].update_one({'email':Auth.email},{"$set":{"organizations":[{"id":ObjectId(org_id)}]}})
        admin = db.instance['users'].find_one({'email': admin['email']})
        request_client['get'](f"/users/verify-email/{admin['organizations'][0]['invitation']['hash']}")
        token_data = request_client['post']('/sign-in/', json=admin_payload, headers=headers)
        headers['Authorization'] = f"Bearer {json.loads(token_data.data)['result']['access_token']}"
        res = request_client['post']("/users/manage-status", json=deactivate_payload, headers=headers)
        assert res.status_code == 200
        user = db.instance['users'].find_one({'email':Auth.email})
        assert user['deactivate']['deactivated_at'] is not None


def testUsersGetsDeactivatedAppwiseInSelectiveMode(accessToken):
    admin = {
        'first_name': 'Saas',
        'last_name': 'Admin',
        'middle_name': 'Middle',
        'company_country': 'INDIA',
        'email': 'admin@saas.com',
        'password': 'iamadmin',
        'company_name': 'Saas'
    }
    role = db.instance['roles'].insert_many([{
        "slug": 'account-saas-role',
        "app_slug": "accounts",
        "name": "Saas Role",
        "default": True,
        "permissions": [
            'accounts~users~all~manage-status'
        ]
    }])
    headers = {"Content-Type": "application/json"}
    app = createApp()
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=admin, headers=headers)
        org_id = json.loads(res.data)['data']['insertedIds']['organization']
        db.instance['users'].update_one({'email': admin['email'], 'organizations.id': ObjectId(org_id)}, {'$set':{
            'organizations.$.accounts.role_ids':[ObjectId(_id) for _id in role.inserted_ids]
        }})
        user = db.instance['users'].find_one({'email': Auth.email})
        deactivate_payload = {
            "ids": [str(user['_id'])],
            "action": "deactivate",
            "use_organization": True,
            "app": "hr"
        }
        admin_payload = {
            'email': admin['email'],
            'password': admin['password'],
            'host_data': {
                'fingerprint': 'Demo'
            }
        }
        db.instance['users'].update_one({'email':Auth.email},{"$set":{"organizations":[{"id":ObjectId(org_id)}]}})
        admin = db.instance['users'].find_one({'email': admin['email']})
        request_client['get'](f"/users/verify-email/{admin['organizations'][0]['invitation']['hash']}")
        token_data = request_client['post']('/sign-in/', json=admin_payload, headers=headers)
        headers['Authorization'] = f"Bearer {json.loads(token_data.data)['result']['access_token']}"
        res = request_client['post']("/users/manage-status", json=deactivate_payload, headers=headers)
        assert res.status_code == 200
        user = db.instance['users'].find_one({'email':Auth.email})
        assert user['organizations'][0]['hr']['deactivate']['deactivated_at'] is not None


def testVerifiesCorrectlyOnFirstInviteFromASpecificApp():
    role_doc = {
      "slug": 'account-owner-role',
      "app_slug": "accounts",
      "name": "Accounts Role",
      "permissions": Auth.permissions,
      "default": True
    }

    db.instance['roles'].insert_one(role_doc)
    payload = {
      "first_name": "Test",
      "company_name": Auth.organization_name,
      "last_name": "Name",
      "middle_name": "Middle",
      "company_country": "INDIA",
      "email" : Auth.email,
      "password" : Auth.password
    }
    app = createApp()
    headers = {"Content-Type": "application/json"}
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=payload, headers=headers)
        data = json.loads(res.data)['data']
        user = db.instance['users'].find_one({"_id":ObjectId(data['insertedIds']['user'])})
        db.instance['users'].update_one({'_id':user['_id'],'organizations.id':user['organizations'][0]['id']},{"$set":{"organizations.$.hr.invitation":user['organizations'][0]['invitation']}})
        db.instance['users'].update_one({'_id':user['_id'],'organizations.id':user['organizations'][0]['id']},{"$unset":{'organizations.$.invitation':user['organizations'][0]['invitation']}})
        payload = {
            'password': 'Test@1234',
            'confirm_password': 'Test@1234',
            'token': user['organizations'][0]['invitation']['hash']
        }
        res = request_client['post']('/users/set-password', json=payload, headers=headers)
        assert res.status_code == 200
        assert json.loads(res.data)['status'] is True

    
def testUserOrganizationListingWhichShouldReturnYes(accessToken):
    # Should return yes for hr accepted invite
    pp = pprint.PrettyPrinter(indent=4)
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    organization = db.instance['organizations'].find_one({})

    db.instance['app_registrations'].insert_one({
        "workspace": "test-hr",
        "org_id": organization['_id']
    })

    db.instance['users'].update_one({ 'organizations.id': organization['_id'] }, {
        '$set': {
            'organizations.$.hr': {
                'role_ids': [],
                'invitation': {
                    'hash': None
                },
            
            },
            'organizations.$.invitee_id': ObjectId(),
            'organizations.$.invitation': None
        }
    })
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        
        assert len(result['data']) == 1
        organizations = result['data'][0]['organizations'][0]
        assert organizations['hr_has_accepted_invite'] is True
        assert organizations['has_accepted_invite'] is False
        


def testUserOrganizationsShouldReturnFalseForHR(accessToken):
    pp = pprint.PrettyPrinter(indent=4)
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    organization = db.instance['organizations'].find_one({})

    db.instance['app_registrations'].insert_one({
        "workspace": "test-hr",
        "org_id": organization['_id']
    })

    db.instance['users'].update_one({ 'organizations.id': organization['_id'] }, {
        '$set': {
            'organizations.$.hr': {
                'role_ids': [],
                'invitation': None,
            },
            'organizations.$.invitee_id': ObjectId(),
            'organizations.$.invitation': None
        }
    })
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        
        assert len(result['data']) == 1
        organizations = result['data'][0]['organizations'][0]
        assert organizations['hr_has_accepted_invite'] is False
        assert organizations['has_accepted_invite'] is False

def testUserOrganizationsShouldReturnFalseForBoth(accessToken):
    pp = pprint.PrettyPrinter(indent=4)
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    organization = db.instance['organizations'].find_one({})

    db.instance['app_registrations'].insert_one({
        "workspace": "test-hr",
        "org_id": organization['_id']
    })

    db.instance['users'].update_one({ 'organizations.id': organization['_id'] }, {
        '$set': {
            'organizations.$.hr': {
                'role_ids': []
            },
            'organizations.$.invitee_id': ObjectId(),
            'organizations.$.invitation': None
        }
    })
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)

        assert len(result['data']) == 1
        organizations = result['data'][0]['organizations'][0]
        assert organizations['hr_has_accepted_invite'] is False
        assert organizations['has_accepted_invite'] is False

def testUserOrganizationsProcessingWithNumPy4(accessToken):
    pp = pprint.PrettyPrinter(indent=4)
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    organization = db.instance['organizations'].find_one({})

    db.instance['app_registrations'].insert_one({
        "workspace": "test-hr",
        "org_id": organization['_id']
    })

    db.instance['users'].update_one({ 'organizations.id': organization['_id'] }, {
        '$set': {
            'organizations.$.invitation': None,
            'organizations.$.invitee_id': ObjectId()
        }
    })
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        
        assert len(result['data']) == 1
        organizations = result['data'][0]['organizations'][0]
        assert organizations['hr_has_accepted_invite'] is False
        assert organizations['has_accepted_invite'] is False

def testUserOrganizationsProcessingWithNumPy5(accessToken):
    pp = pprint.PrettyPrinter(indent=4)
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    organization = db.instance['organizations'].find_one({})

    db.instance['app_registrations'].insert_one({
        "workspace": "test-hr",
        "org_id": organization['_id']
    })

    db.instance['users'].update_one({ 'organizations.id': organization['_id'] }, {
        '$set': {
            'organizations.$.invitation': {
                'hash': 'asd'
            },
            'organizations.$.invitee_id': ObjectId()
        }
    })
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        
        assert len(result['data']) == 1
        organizations = result['data'][0]['organizations'][0]
        assert organizations['hr_has_accepted_invite'] is False
        assert organizations['has_accepted_invite'] is False


def testUserOrganizationsProcessingWithNumPy6(accessToken):
    pp = pprint.PrettyPrinter(indent=4)
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    app = createApp()
    organization = db.instance['organizations'].find_one({})

    db.instance['app_registrations'].insert_one({
        "workspace": "test-hr",
        "org_id": organization['_id']
    })

    db.instance['users'].update_one({ 'organizations.id': organization['_id'] }, {
        '$set': {
            'organizations.$.invitation': {
                'hash': None
            },
            'organizations.$.invitee_id': ObjectId()
        }
    })
    with app.test_client() as client:
        request_client = Client(client)
        response = request_client["get"](f'{BASE_URL}/organizations', headers=headers)
        result = json.loads(response.data)
        
        assert len(result['data']) == 1
        organizations = result['data'][0]['organizations'][0]
        assert organizations['hr_has_accepted_invite'] is False
        assert organizations['has_accepted_invite'] is True


def testLocksSingleUserForSpecificTime(accessToken):
    app = createApp()
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    payload = {
        "first_name": "Test",
        "company_name": "Test Org",
        "last_name": "Name",
        "middle_name": "Middle",
        "company_country": "INDIA",
        "email" : "test@another.com",
        "password" : Auth.password
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=payload, headers=headers)
        user_id = json.loads(res.data)['data']['insertedIds']['user']
        payload = {
            "ids": [user_id],
            "lock_action": "lock",
            "locked_indefinite": False,
            "lock_duration": 20,
            "lock_type": "days"
        }
        result = request_client['post']('/users/manage-lock', json=payload, headers=headers)
        assert result.status_code == 200
        user = db.instance['users'].find_one({"_id":ObjectId(user_id)})
        assert user['lock']['status'] == "admin-lock"
        assert (datetime.now()+timedelta(days=20)).strftime("%d-%m-%Y") == user['lock']['lock_time'].strftime("%d-%m-%Y")


def testLocksSingleUserPermanently(accessToken):
    app = createApp()
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    payload = {
      "first_name": "Test",
      "company_name": "Test Org",
      "last_name": "Name",
      "middle_name": "Middle",
      "company_country": "INDIA",
      "email" : "test@another.com",
      "password" : Auth.password
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=payload, headers=headers)
        print(res.data)
        user_id = json.loads(res.data)['data']['insertedIds']['user']
        payload = {
            "ids": [user_id],
            "lock_action": "lock",
            "locked_indefinite": True,
        }
        result = request_client['post']('/users/manage-lock', json=payload, headers=headers)
        assert result.status_code == 200
        user = db.instance['users'].find_one({"_id":ObjectId(user_id)})
        assert user['lock']['lock_time'] is None
        assert user['lock']['status'] == "admin-lock"


def testLocksUsersForSpecificTime(accessToken):
    app = createApp()
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    payload = {
        "first_name": "Test",
        "company_name": "Test Org",
        "last_name": "Name",
        "middle_name": "Middle",
        "company_country": "INDIA",
        "email" : "test@another.com",
        "password" : Auth.password
    }
    with app.test_client() as client:
        request_client = Client(client)
        request_client['post']('/sign-up/', json=payload, headers=headers)
        payload['email'] = "test@another2.com"
        request_client['post']('/sign-up/', json=payload, headers=headers)
        user_docs = list(db.instance['users'].find({"email":{"$in":["test@another.com","test@another2.com"]}}))
        ids = [str(doc['_id']) for doc in user_docs]
        payload = {
            "ids": ids,
            "lock_action": "lock",
            "locked_indefinite": False,
            "lock_duration": 20,
            "lock_type": "days"
        }
        result = request_client['post']('/users/manage-lock', json=payload, headers=headers)
        assert result.status_code == 200
        users = db.instance['users'].find({"_id":{"$in":[ObjectId(id) for id in ids]}})
        for user in users:
            assert user['lock']['status'] == "admin-lock"
            assert (datetime.now()+timedelta(days=20)).strftime("%d-%m-%Y") == user['lock']['lock_time'].strftime("%d-%m-%Y")


def testLocksUsersPermanently(accessToken):
    app = createApp()
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    payload = {
      "first_name": "Test",
      "company_name": "Test Org",
      "last_name": "Name",
      "middle_name": "Middle",
      "company_country": "INDIA",
      "email" : "test@another.com",
      "password" : Auth.password
    }
    with app.test_client() as client:
        request_client = Client(client)
        request_client['post']('/sign-up/', json=payload, headers=headers)
        payload['email'] = "test@another2.com"
        request_client['post']('/sign-up/', json=payload, headers=headers)
        user_docs = list(db.instance['users'].find({"email":{"$in":["test@another.com","test@another2.com"]}}))
        ids = [str(doc['_id']) for doc in user_docs]
        payload = {
            "ids": ids,
            "lock_action": "lock",
            "locked_indefinite": True,
        }
        result = request_client['post']('/users/manage-lock', json=payload, headers=headers)
        assert result.status_code == 200
        users = db.instance['users'].find({"_id":{"$in":[ObjectId(id) for id in ids]}})
        for user in users:
            assert user['lock']['lock_time'] is None
            assert user['lock']['status'] == "admin-lock"


def testUnlockWorksOnMultipleUsers(accessToken):
    app = createApp()
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    payload = {
      "first_name": "Test",
      "company_name": "Test Org",
      "last_name": "Name",
      "middle_name": "Middle",
      "company_country": "INDIA",
      "email" : "test@another.com",
      "password" : Auth.password
    }
    with app.test_client() as client:
        request_client = Client(client)
        request_client['post']('/sign-up/', json=payload, headers=headers)
        payload['email'] = "test@another2.com"
        request_client['post']('/sign-up/', json=payload, headers=headers)
        db.instance['users'].update_many({"email": {"$in":["test@another.com","test@another2.com"]}},{"$set":{'lock':{
            "lock_time" : None,
            # "locked_by" : request.environ['jwt_data']["token"]["userInfo"]["id"],
            "locked_by": None,
            "locked_at" : datetime.now(),
            "status"    : "admin-lock",
        },'status':3,'status_stack':[3]}})
        res = list(db.instance['users'].find({"email":{"$in":["test@another.com","test@another2.com"]}}))
        ids = [str(doc['_id']) for doc in res]
        print(ids)
        payload = {
            "ids": ids,
            "lock_action": "unlock",
        }
        res = request_client['post']('/users/manage-lock', json=payload, headers=headers)
        assert res.status_code == 200
        users = db.instance['users'].find({"_id":{"$in":[ObjectId(id) for id in ids]}})
        for user in users:
            assert user['lock'] is not None
            assert len(user['lock']) == 0


def testUnlockWorksOnMultipleUsers(accessToken):
    app = createApp()
    headers = {'Authorization': f'Bearer {accessToken}', "Content-Type": "application/json"}
    payload = {
      "first_name": "Test",
      "company_name": "Test Org",
      "last_name": "Name",
      "middle_name": "Middle",
      "company_country": "INDIA",
      "email" : "test@another.com",
      "password" : Auth.password
    }
    with app.test_client() as client:
        request_client = Client(client)
        res = request_client['post']('/sign-up/', json=payload, headers=headers)
        _id = json.loads(res.data)['data']['insertedIds']['account']
        lock = {
            "lock_time": datetime.now() + timedelta(days=2),
            "locked_by": None,
            "locked_at": datetime.now(),
            "status": "admin-lock"
        }
        db.instance['accounts'].find_one_and_update({"_id":ObjectId(_id)},{"$set":{"lock":lock}})
        payload = {
            "ids": [_id],
            "lock_action": "unlock"
        }
        res = request_client['post']('/accounts/manage-lock', json=payload, headers=headers)
        print(res.data)
        assert res.status_code == 200
        accounts = list(db.instance['accounts'].find({"_id":ObjectId(_id)}))
        for account in accounts:
            assert len(account['lock']) == 0
            assert account['status'] == 1
            assert 3 not in account['status_stack']
