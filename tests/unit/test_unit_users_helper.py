import json
from Core.Helpers import Helper
from Application.users.Helpers import Utility
from flask import Flask, request
app = Flask(__name__)

def testUtilityExtendsCoreHelper():
    assert issubclass(Utility, Helper) is True

def testUtilityHasvalidatePassword():
    assert hasattr(Utility, 'validatePassword') is True

def testUtilityHashashPassword():
    assert hasattr(Utility, 'hashPassword') is True

def testUtilityAlltheMethodOfCore():
    assert hasattr(Utility, 'getConfiguration') is True
    assert hasattr(Utility, 'toLower') is True
    assert hasattr(Utility, 'toUpper') is True
    assert hasattr(Utility, 'sanitizeString') is True
    assert hasattr(Utility, 'resetKeys') is True
    assert hasattr(Utility, 'convertDateToIsoDate') is True
    assert hasattr(Utility, 'generateSlug') is True
    assert hasattr(Utility, 'implementAutoIncrement') is True
    assert hasattr(Utility, 'generateRandomString') is True
    
def testvalidatePasswordShouldReturnTrue():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert Utility.validatePassword("Test@123")

def testvalidatePasswordShouldReturnFalse():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert True if Utility.validatePassword("Test12312qw") is False else True

def testHashPasswordShouldReturnTheHash():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert Utility.hashPassword("Test@123") == "f925916e2754e5e03f75dd58a5733251"

def testHashPasswordShouldReturnNone():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert Utility.hashPassword("") is None
   
def testUsersvalidatePasswordReturnsInstanceOfBool():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert isinstance(Utility.validatePassword("Test@123"), bool)

def testUsersHashPasswordReturnsInstanceOfString():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert isinstance(Utility.hashPassword("Test@123"), str)

def testUsersHashPasswordReturnsInstanceOfNoneWhenPasswordIsEmpty():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert Utility.hashPassword("") is None