import json
from Core.Helpers import Helper
from Application.ip_addresses.Helpers import Utility
from flask import Flask, request
app = Flask(__name__)

def testUtilityExtendsCoreHelper():
    assert issubclass(Utility, Helper) is True

def testUtilityHasvalidatePassword():
    assert hasattr(Utility, 'validateIP') is True
def testvalidateIPShouldReturnTrue():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert Utility.validateIP("192.123.12.1")

def testvalidateIPShouldReturnFalse():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        assert True if Utility.validateIP("0000.000.00.00") is False else True

def testvalidateIPShouldReturnBooleans():
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        response = Utility.validateIP("0000.000.00.00")
        assert isinstance(response, bool)