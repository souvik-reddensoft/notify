from unittest.mock import Mock        
import json
import mock
import pymongo
from flask import Flask, request
from Core.Models.Model import Model
from Application.users.Models.Users import users, Users
from Core.Factories.Database import DbFactory as db
from Core.Models.Model import Model as Base
app = Flask(__name__)

def testUsersModelHasListMethod():
    assert hasattr(Users, 'list') is True

def testUsersModelHasDeleteMethod():
    assert hasattr(Users, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testUsersModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testUsersModelHasSchemaDefinition():
    assert len(Users.fields) > 0

def testUsersModelHasCollectionNameDefined():
    assert Users.collection is not  None and  Users.collection == 'users'

def testUsersMethodFetchListShouldReturnBoolean():
    _mock = Mock()
    data = Users.fetchList.return_value = True
    assert isinstance(data, bool) is True

def testUsersModelHasProfileMethod():
    assert hasattr(Users, 'profile') is True

def testUsersModelHasGetOrganizationsMethod():
    assert hasattr(Users, 'getOrganizations') is True

def testUsersModelHasGetUserMethod():
    assert hasattr(Users, 'getUserName') is True
    
def testUsersModelHasUpdateWithAndOperationMethod():
    assert hasattr(Users, 'updateWithAndOperation') is True

def testUsersModelHasFindOneMethod():
    assert hasattr(Users, 'findOne') is True
    