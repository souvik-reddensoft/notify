from unittest.mock import Mock
import mock
from flask import Flask
from Core.Models.Model import Model
from Application.accounts.Models.Accounts import Accounts
app = Flask(__name__)

def testAccountsModelHasListMethod():
    assert hasattr(Accounts, 'list') is True

def testAccountsModelHasDeleteMethod():
    assert hasattr(Accounts, 'delete') is True

@mock.patch.object(Model, '__init__',return_value = None)
def testAccountsModelHasBaseModelExtended(mock_base_init):
    assert Model().__init__.called

def testAccountsModelHasSchemaDefinition():
    assert len(Accounts.fields) > 0

def testAccountsModelHasCollectionNameDefined():
    assert Accounts.collection is not None and  Accounts.collection == 'accounts'

def testAccountsModelHasViewDefinition():
    assert hasattr(Accounts, 'view') is True