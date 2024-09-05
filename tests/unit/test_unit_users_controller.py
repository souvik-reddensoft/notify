import json
from unittest.mock import MagicMock
import mock
import datetime
from werkzeug.exceptions import NotFound, BadRequest
from flask import Flask, request
from Application.signup.Helpers import Helper as SignupHelper
from Core.Controllers.Controller import Controller
from Application.users.Controllers.Users import users, Users as UsersClass
from Application.users.Models.Users import Users
from Application.users.Helpers import Utility
from Application.signin.Helpers import Helper as SigninHelper
from Application.accounts.Models.Accounts import Accounts
from Application.users.Helpers.NotificationManage import NotificationManage
from Application.roles.Controllers.Role import role
app = Flask(__name__)

def testUsersControllerExtendsBaseController():
    assert issubclass(UsersClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfUsersModel():
    assert isinstance(users.model, Users) is True

def testUsersControllerHasListMethod():
    assert hasattr(UsersClass, 'list') is True

def testUsersControllerHasCreateMethod():
    assert hasattr(UsersClass, 'create') is True

def testUsersControllerHasUpdateMethod():
    assert hasattr(UsersClass, 'update') is True

def testUsersControllerHasDeleteMethod():
    assert hasattr(UsersClass, 'delete') is True

def testUsersControllerHasDestroyMethod():
    assert hasattr(UsersClass, 'destroy') is True

def testUsersControllerHasViewMethod():
    assert hasattr(UsersClass, 'view') is True

def testUsersControllerHasTrashMethod():
    assert hasattr(UsersClass, 'trash') is True

def testUsersControllerHasRestoreMethod():
    assert hasattr(UsersClass, 'restore') is True
    
def testExtendsBaseController():
    assert issubclass(UsersClass, Controller) is True

def testHasModelAttributeWhichIsInstanceOfUsersModel():
    assert isinstance(users.model, Users) is True

@mock.patch.object(Users, 'list')
def testUsersModelListIsCalledInUsersControllerList(mock_list_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        users.list()
        assert Users().list.called

@mock.patch.object(Users, 'create')
def testUserModelCreateIsCalledInUsersControllerCreate(mock_create_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.create()
        assert users.validate.called
        assert Users().create.called

@mock.patch.object(Users, 'isDeleted', return_value = None)
@mock.patch.object(Users, 'update')
def testUsersModelUpdateIsCalledInUsersControllerUpdate(mock_update_method, mock_is_deleted_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.update('1234')
        assert users.validate.called
        assert Users().isDeleted.called
        assert Users().update.called

@mock.patch.object(Users, 'isDeleted', return_value = None)
@mock.patch.object(Users, 'delete')
def testUsersModelDeleteIsCalledInUsersControllerDelete(mock_delete_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.delete('1234')
        assert Users().isDeleted.called
        assert Users().delete.called

@mock.patch.object(Users, 'isDeleted', return_value = {})
@mock.patch.object(Users, 'restore')
def testUsersModelRestoreIsCalledInUsersControllerRestore(mock_restore_method, mock_is_deleted_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.restore('1234')
        assert Users().isDeleted.called
        assert Users().restore.called

@mock.patch.object(Users, 'find', return_value = {})
@mock.patch.object(Users, 'destroy', return_value = 1)
def testUsersModelDestroyIsCalledInUsersControllerDestroy(mock_destroy_method, mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        users.destroy('1234')
        assert Users().find.called # pylint: disable=E1101
        assert Users().destroy.called # pylint: disable=E1101

@mock.patch.object(Users, 'find', return_value = {'email': 'test@test.com'})
def testUserModelFindIsCalledInUsersControllerGenerateQrCode(mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        request.environ = _mock
        users.generateQrCode()
        assert Users().find.called # pylint: disable=E1101

@mock.patch.object(Users, 'find', return_value = {'email': 'test@test.com'})
def testQrCodeSvgIsReturnedInUsersControllerGenerateQrCode(mock_find_method):
    with app.test_request_context():
        _mock = MagicMock()
        request.t = _mock
        request.environ = _mock
        result = users.generateQrCode()
        assert len(result['data']['qr']) > 0 # pylint: disable=E1101
        
@mock.patch.object(Users, 'updateWithAndOperation', return_value = {})
def testUserschangePasswordMethodCalledValidateMethod(mock_getUser_method):
    with app.test_request_context(data = json.dumps({"current_password":"CUtpiq@L+3G@","password":"CUtpiq@L+3G@#","confirm_password" : "CUtpiq@L+3G@#"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        users.changePassword("6385a3c6ad12d12c96dbb4d4")
        assert users.validate.called

@mock.patch.object(UsersClass, 'changePassword', return_value = {})
def testUsersResetPasswordMethodCalledControllerChangePasswordMethod(mock_changePassword_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        users.changePassword()
        assert UsersClass().changePassword.called

@mock.patch.object(users, 'verifyEmail', return_value = {"data": {},"message": "Account created successfully"})
@mock.patch.object(Utility, 'hashPassword', return_value = 'S7S6t5J9xbz7R4t5e3P3Ueq2O2E55e7e5795352d0d786316')
def testUsersControllerverifyEmailIsCalledInUsersControllersetPassword(mock_hashPassword_method, mock_verifyemail_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@", "confirm_password" : "CUtpiq@L+3G@#", "token":"S7S6t5J9xbz7R4t5e3P3Ueq2O2E55e7e5795352d0d786316"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        users.validate = _mock
        users.setPassword()
        assert users.validate.called # pylint: disable=E1101
        assert Utility.hashPassword.called # pylint: disable=E1101
        assert users.verifyEmail.called

@mock.patch.object(Users, 'fetchList', return_value = {"results":{"results_count": 1, "results": {"data": [{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testgeneratePasswordResetLinkMethod(mock_fetchlist_method, mock_update_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.generatePasswordResetLink()
        assert Users().fetchList.called
        assert Users().update.called
        assert users.validate.called
        assert NotificationManage("test@codeclouds.com", "Notification Body").send.called

@mock.patch.object(Users, 'fetchList', return_value = {"results":{"results_count": 0, "results": {"data": [{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testgeneratePasswordResetLinkMethodThrowException(mock_fetchlist_method, mock_update_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        try:
            users.generatePasswordResetLink()
        except Exception as ex:
            assert True

@mock.patch.object(Users, 'fetchList', return_value = {"results":{"results_count": 0, "results": {"data": [{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testgeneratePasswordResetLinkMethodThrowException(mock_fetchlist_method, mock_update_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        try:
            users.generatePasswordResetLink()
            assert False
        except Exception as ex:
            assert True

@mock.patch.object(Users, 'updateWithAndOperation', return_value = None)
def testUserschangePasswordMethodShouldThrowsExceptionWhenUserDataISNone(mock_getUser_method):
    with app.test_request_context(data = json.dumps({"current_password":"CUtpiq@L+3G@","password":"CUtpiq@L+3G@#","confirm_password" : "CUtpiq@L+3G@#"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        try:
            users.changePassword("6385a3c6ad12d12c96dbb4d4")
            assert False
        except Exception as ex:
            assert True
       
@mock.patch.object(Users, 'profile', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4", "email": "test@codeclouds.com", "image": "https://www.istockphoto.com/photo/group-of-business-people-standing-in-hall-smiling-and-talking-together-gm530685719-530685719?utm_source=pixabay&utm_medium=affiliate&utm_campaign=SRP_image_sponsored&utm_content=https%3A%2F%2Fpixabay.com%2Fimages%2Fsearch%2Flink%2F&utm_term=link"})
@mock.patch.object(Utility, 'hashPassword', return_value = {})
def testUsersProfileCalledModelProfile(mock_profile_method, mock_hashPassword_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        request.environ["jwt_data"] = _mock
        users.profile()
        Users().profile.called
        Utility.hashPassword.called

@mock.patch.object(users, 'update', return_value = {})
def testSaveProfileCalledControllerUpdateMethod(mock_profile_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        request.environ["jwt_data"] = _mock
        users.saveProfile()
        assert users.update.called

@mock.patch.object(users, 'update', return_value = {})
def testSaveProfileReturnsTypeIsInstanceOfDict(mock_save_profile_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        request.environ["jwt_data"] = _mock
        assert isinstance(users.saveProfile(), dict)

@mock.patch.object(Users, 'profile', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4", "email": "test@codeclouds.com", "image": "https://www.istockphoto.com/photo/group-of-business-people-standing-in-hall-smiling-and-talking-together-gm530685719-530685719?utm_source=pixabay&utm_medium=affiliate&utm_campaign=SRP_image_sponsored&utm_content=https%3A%2F%2Fpixabay.com%2Fimages%2Fsearch%2Flink%2F&utm_term=link"})
def testProfileReturnsTypeIsInstanceOfDict(mock_save_profile_method):
    with app.test_request_context(data = json.dumps({}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        request.environ["jwt_data"] = _mock
        assert isinstance(users.profile(), dict)

@mock.patch.object(Users, 'fetchList', return_value = {"results":{"results_count": 1, "results": {"data": [{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testgeneratePasswordResetLinkMethod(mock_fetchlist_method, mock_update_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        assert isinstance(users.generatePasswordResetLink(), dict)
        
@mock.patch.object(Users, 'updateWithAndOperation', return_value = {})
@mock.patch.object(Users, 'getSchema', return_value = {})
@mock.patch.object(Utility, 'hashPassword', return_value = {})
def testUserschangePasswordMethodCalledUsersModelupdateWithAndOperationMethod(mock_getUser_method, mock_getSchema_method, mock_HashPassword_method):
    with app.test_request_context(data = json.dumps({"current_password":"CUtpiq@L+3G@","password":"CUtpiq@L+3G@#","confirm_password" : "CUtpiq@L+3G@#"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        assert isinstance(users.changePassword("6385a3c6ad12d12c96dbb4d4"), dict)

@mock.patch.object(UsersClass, 'changePassword', return_value = {})
def testUsersResetPasswordMethodCalledControllerChangePasswordMethod(mock_changePassword_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        assert isinstance(users.changePassword(), dict)

@mock.patch.object(users, 'verifyEmail', return_value = {"data": {},"message": "Account created successfully"})
@mock.patch.object(Utility, 'hashPassword', return_value = 'S7S6t5J9xbz7R4t5e3P3Ueq2O2E55e7e5795352d0d786316')
def testUsersControllerverifyEmailIsCalledInUsersControllersetPassword(mock_hashPassword_method, mock_verifyemail_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@", "confirm_password" : "CUtpiq@L+3G@#", "token":"S7S6t5J9xbz7R4t5e3P3Ueq2O2E55e7e5795352d0d786316"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        users.validate = _mock
        assert isinstance(users.setPassword(), dict)

@mock.patch.object(role.model, 'fetchList', return_value = {"results": {"results": {"data":[{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(Users, 'fetchList', return_value = {})
@mock.patch.object(Users, 'getUserName', return_value = {})
def testGetAccountManagerReturnDict(mock_role_fetchList_method, mock_user_fetchList_method, mock_getUserName_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        assert isinstance(users.getAccountManager(), dict)

@mock.patch.object(Users, 'getUser', return_value = {"results": {"results_count": 1, "results": {"data":[{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(UsersClass, 'changePassword', return_value = {})
def testUsersResetPasswordMethodCalledModelGetUserMethod(mock_getUser_method, mock_changePassword_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        assert isinstance(users.resetPassword(), dict)

@mock.patch.object(Users, 'find', return_value={})
@mock.patch.object(Users, 'update')
@mock.patch.object(SigninHelper, 'verifyTOTP', return_value=True)
@mock.patch.object(Utility, 'generateRecoveryCodes', return_value=[])
def testCallsModelFindAndModelUpdateInUsersControllerActivateAuthenticatorApp(mock_recoverygenerate_method, mock_verifyotp_method, mock_update_method, mock_find_method):
    with app.test_request_context(data=json.dumps({'secret':'fwagwag','code':'fwafawgwag'}),method='POST' ,content_type='application/json'):
        _mock = MagicMock()
        users.validate = _mock
        request.t = _mock
        request.environ['jwt_data'] = _mock
        users.activateAuthenticatorApp()
        assert Users().find.called # pylint: disable=E1101
        assert Users().update.called # pylint: disable=E1101

@mock.patch.object(Users, 'find', return_value={})
@mock.patch.object(Users, 'update')
@mock.patch.object(SigninHelper, 'verifyTOTP', return_value=True)
@mock.patch.object(Utility, 'generateRecoveryCodes', return_value=[])
def testCallsSigninHelperVerifyTOTPInUsersControllerActivateAuthenticatorApp(mock_recoverygenerate_method, mock_verifyotp_method, mock_update_method, mock_find_method):
    with app.test_request_context(data=json.dumps({'secret':'fwagwag','code':'fwafawgwag'}),method='POST' ,content_type='application/json'):
        _mock = MagicMock()
        users.validate = _mock
        request.t = _mock
        request.environ['jwt_data'] = _mock
        users.activateAuthenticatorApp()
        assert SigninHelper.verifyTOTP.called # pylint: disable=E1101

@mock.patch.object(Users, 'find', return_value={})
@mock.patch.object(Users, 'update')
@mock.patch.object(Users, 'destroy')
@mock.patch.object(SigninHelper, 'verifyTOTP', return_value=True)
@mock.patch.object(Utility, 'generateRecoveryCodes', return_value=[])
def testCallsHelperGenerateRecoveryCodesInUsersControllerActivateAuthenticatorApp(mock_recoverygenerate_method, mock_verifyotp_method, mock_destroy_method, mock_update_method, mock_find_method):
    with app.test_request_context(data=json.dumps({'secret':'fwagwag','code':'fwafawgwag'}),method='POST' ,content_type='application/json'):
        _mock = MagicMock()
        users.validate = _mock
        request.t = _mock
        request.environ['jwt_data'] = _mock
        users.activateAuthenticatorApp()
        assert Utility().generateRecoveryCodes.called # pylint: disable=E1101
        assert users.validate.called

@mock.patch.object(Users, 'update')
@mock.patch.object(Utility, 'generateRandomStringSet', return_value=[])
@mock.patch.object(Utility, 'generateRandomString', return_value=[])
def testUsersRegenerateRecoveryCodeMethodCalledHelperMethodsAndModelUpdateMethod(mock_update_method, mock_generateRandomStringSet_method, mock_generateRandomString_method):
    with app.test_request_context(data=json.dumps({}),method='POST' ,content_type='application/json'):
        _mock = MagicMock()
        users.validate = _mock
        request.t = _mock
        request.environ['jwt_data'] = _mock
        users.regenerateRecoveryCode()
        assert Utility().generateRandomStringSet.called # pylint: disable=E1101
        assert Utility().generateRandomString.called # pylint: disable=E1101
        assert Users().update.called # pylint: disable=E1101

@mock.patch.object(Users, 'update')
@mock.patch.object(Utility, 'generateRandomStringSet', return_value=[])
@mock.patch.object(Utility, 'generateRandomString', return_value=[])
def testUsersRegenerateRecoveryCodeMethodReturnsDict(mock_update_method, mock_generateRandomStringSet_method, mock_generateRandomString_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        assert isinstance(users.regenerateRecoveryCode(), dict)

@mock.patch.object(Users, 'update', return_value = None)
@mock.patch.object(Utility, 'generateRandomStringSet', return_value=[])
@mock.patch.object(Utility, 'generateRandomString', return_value=[])
def testUsersRegenerateRecoveryCodeMethodThrowsException(mock_update_method, mock_generateRandomStringSet_method, mock_generateRandomString_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        try:
            users.regenerateRecoveryCode()
            assert False
        except Exception as ex:
            assert True if (isinstance(ex, NotFound)) else False

@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret"} })
@mock.patch.object(Users, 'update', return_value = {})
def testDisable2FAMethodCalledValidatorAndModeFindMethod(mock_find_method, mock_update_method):
    with app.test_request_context(data = json.dumps({"type": "sms"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.disable2FA()
        Users().find.called
        users.validate.called

@mock.patch.object(Users, 'find', return_value = None)
@mock.patch.object(Users, 'update', return_value = {})
def testDisable2FAMethodCalledMethodThrowsExceptionWhenUserNotFound(mock_find_method, mock_update_method):
    with app.test_request_context(data = json.dumps({"type": 'sms'}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        try:
            users.disable2FA()
            assert False
        except NotFound as ex:
            assert True

@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret"} })
@mock.patch.object(Users, 'update', return_value = {})
def testDisable2FAMethodCalledModelUpdateMethodWhenTypeIsSms(mock_find_method, mock_update_method):
    with app.test_request_context(data = json.dumps({"type": "sms"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        response = users.disable2FA()
        Users().update.called

@mock.patch.object(Users, 'find', return_value =  {"_id" : "62724297f3b2a095b37f9801", "2fa": {"secret": "some secret", "temp_sms_data": {"otp": "8976", "phone": "9898989898", "isd": "91"}}} )
@mock.patch.object(Users, 'update', return_value = {})
def testDisable2FAMethodCalledModelUpdateMethodWhenTypeIsSmsWithOtp(mock_find_method, mock_update_method):
    with app.test_request_context(data = json.dumps({"type": "sms", "otp" : "8976"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        response = users.disable2FA()
        Users().update.called

@mock.patch.object(SigninHelper, 'verifyTOTP', return_value = True)
@mock.patch.object(Users, 'find', return_value = {"_id" : "62724297f3b2a095b37f9801", "2fa": {"secret": "some secret"} })
@mock.patch.object(Users, 'update', return_value = {})
def testDisable2FAMethodCalledModelUpdateMethodWhenTypeIsAuthenticatorApp(mock_find_method, mock_update_method, mock_verifyotp_method):
    with app.test_request_context(data = json.dumps({"type": "authenticator-app", 'code':'dfgfhghjyuty'}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        response = users.disable2FA()
        Users().update.called

# @mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret"} })
# @mock.patch.object(Users, 'update', return_value = {})
# def testDisable2FAMethodCalledModelUpdateMethodWhenTypeIsAll(mock_find_method, mock_update_method):
#     with app.test_request_context(data = json.dumps({"type": "authenticator-app"}), content_type='application/json'):
#         _mock = MagicMock()
#         request.environ["jwt_data"] = _mock
#         request.t = _mock
#         response = users.disable2FA()
#         Users().update.called
        
@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret"} })
@mock.patch.object(Users, 'update', return_value = {})
def testDisable2FAMethodCalledMethodThrowsExceptionWhenTypeIS_(mock_find_method, mock_update_method):
    with app.test_request_context(data = json.dumps({"type": '_'}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        try:
            users.disable2FA()
            assert False
        except BadRequest as ex:
            assert True

@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret", "temp_sms_data": {"otp": "8976", "phone": "9898989898", "isd": "91"}} })
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(Utility, 'getSchema', return_value = {})
@mock.patch.object(Utility, 'generateRecoveryCodes', return_value = {})
def testActivateSMS2FACalledModelAndValidator(mock_find_method, mock_update_method, mock_getSchema_method, mock_generateRecoveryCodes_method):
    with app.test_request_context(data = json.dumps({"identifier":"test","phone_number": '9887766554', "isd_code": "91", "otp": "8976", "primary": True}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.activateSMS2FA()
        assert Users().update.called
        assert Users().find.called
        assert users.validate.called

@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret"} })
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(Utility, 'generateRandomString', return_value = "9876")
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testActivateSMS2FACalledUtilityGenerateRandomStringWhenOtpIsNotInRequest(mock_find_method, mock_update_method, mock_utility_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({"phone_number": '9887766554', "isd_code": "91", "primary": True}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.activateSMS2FA()
        assert Users().update.called
        assert Utility().generateRandomString.called
        assert NotificationManage("test@codeclouds.com", "Hello").send.called

@mock.patch.object(Users, 'find', return_value = None)
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(Utility, 'generateRandomString', return_value = "9876")
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testActivateSMS2FAThrowsExceptionWhenUserNotFound(mock_find_method, mock_update_method, mock_utility_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({"phone_number": '9887766554', "isd_code": "91", "primary": True, "otp": "8976"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        try:
            users.activateSMS2FA()
            assert Users().find.called
            assert False
        except Exception as ex:
            assert True
            
@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret", "temp_sms_data": {"otp": "8976", "phone": "9898989898", "isd": "91"}} })
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(Utility, 'generateRandomString', return_value = "9876")
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testActivateSMS2FAThrowsExceptionWhenTempSmsDataIsNone(mock_find_method, mock_update_method, mock_utility_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({"phone_number": '9887766554', "isd_code": "91", "primary": True, "otp": "8976"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        try:
            users.activateSMS2FA()
            assert Users().find.called
            assert False
        except Exception as ex:
            assert True

@mock.patch.object(Users, 'find', return_value = {"2fa": {"secret": "some secret", "temp_sms_data": {"otp": "8976", "phone": "9898989898", "isd": "91"}} })
@mock.patch.object(Users, 'update', return_value = {})
@mock.patch.object(Utility, 'generateRandomString', return_value = "9876")
@mock.patch.object(NotificationManage, 'send', return_value = {})
def testActivateSMS2FAThrowsExceptionWhenOtpNotMatched(mock_find_method, mock_update_method, mock_utility_method, mock_notification_method):
    with app.test_request_context(data = json.dumps({"phone_number": '9887766554', "isd_code": "91", "primary": True, "otp": "89761"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        try:
            users.activateSMS2FA()
            assert Users().find.called
            assert False
        except Exception as ex:
            assert True
        
@mock.patch.object(Users, 'updateWithAndOperation', return_value = {})
@mock.patch.object(Utility, 'getSchema', return_value = {})
@mock.patch.object(Utility, 'hashPassword', return_value = {})
def testUserschangePasswordMethodCalledUsersModelupdateWithAndOperationMethod(mock_getUser_method, mock_getSchema_method, mock_HashPassword_method):
    with app.test_request_context(data = json.dumps({"current_password":"CUtpiq@L+3G@","password":"CUtpiq@L+3G@#","confirm_password" : "CUtpiq@L+3G@#"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        users.changePassword("6385a3c6ad12d12c96dbb4d4")
        assert Users().updateWithAndOperation.called
        assert Utility().getSchema.called
        assert Utility.hashPassword.called

@mock.patch.object(Users, 'updateWithAndOperation', return_value = {})
def testUsersResetPasswordMethodCalledModelGetUserMethod(mock_updateWithAndOperation_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.changePassword("6385a3c6ad12d12c96dbb4d4")      
        assert Users().updateWithAndOperation.called

@mock.patch.object(Users, 'findOne', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4", "owner_account_id": "6385a3c6ad12d12c96dbb4d4", "status": 0})
@mock.patch.object(Accounts, 'find', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4"})
@mock.patch.object(Accounts, 'update', return_value = {})
@mock.patch.object(Users, 'update', return_value = {})
def testVerifyEmailCalledModelFindOneMethod(mock_findOne_method, mock_find_method, mock_update_method, mock_user_update_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.verifyEmail(SignupHelper.generateVerificationHash("6385a3c6ad12d12c96dbb4d4"), "Test@123")
        assert Users().findOne.called

@mock.patch.object(Users, 'findOne', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4", "owner_account_id": "6385a3c6ad12d12c96dbb4d4", "status": 2})
@mock.patch.object(Accounts, 'find', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4"})
@mock.patch.object(Accounts, 'update', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4"})
@mock.patch.object(Users, 'update', return_value = {})
def testVerifyEmailAccountModelFindAndUpdateMethod(mock_findOne_method, mock_find_method, mock_update_method, mock_user_update_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.verifyEmail(SignupHelper.generateVerificationHash("6385a3c6ad12d12c96dbb4d4"), "Test@123")
        assert Accounts().update.called

@mock.patch.object(Users, 'findOne', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4", "owner_account_id": None, "status": 2})
@mock.patch.object(Accounts, 'find', return_value = {"_id": "6385a3c6ad12d12c96dbb4d4"})
@mock.patch.object(Accounts, 'update', return_value = {})
@mock.patch.object(Users, 'update', return_value = {})
def testVerifyEmailUserUpdateMethod(mock_findOne_method, mock_find_method, mock_update_method, mock_user_update_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.verifyEmail(SignupHelper.generateVerificationHash("6385a3c6ad12d12c96dbb4d4"), "Test@123")
        assert Users().update.called

@mock.patch.object(Users, 'fetchList', return_value = {})
def testUsersResetPasswordMethodThrowsExceptionWhenUserInfoIsMissing(mock_changePassword_method):
    with app.test_request_context(data = json.dumps({"password":"CUtpiq@L+3G@","confirm_password":"CUtpiq@L+3G@","token" : "1111"}), content_type='application/json'):
        _mock = MagicMock()
        request.t = _mock
        try:
            users.changePassword()
            assert False
        except Exception as ex:
            assert True

@mock.patch.object(role.model, 'fetchList', return_value = {"results": {"results": {"data":[{"_id": "6385a3c6ad12d12c96dbb4d4"}]}}})
@mock.patch.object(Users, 'fetchList', return_value = {})
@mock.patch.object(Users, 'getUserName', return_value = {})
@mock.patch.object(Utility, 'getFetchListFilter', return_value = {})
def testGetAccountManagerRoleModelFetchlistAndUserModelFetchlistMethodCalled(mock_role_fetchList_method, mock_user_fetchList_method, mock_getUserName_method, mock_getFetchListFilter_method):
    with app.test_request_context(data = json.dumps({"email":"test@codeclouds.com"}), content_type='application/json'):
        _mock = MagicMock()
        request.environ["jwt_data"] = _mock
        request.t = _mock
        users.validate = _mock
        users.getAccountManager()
        assert role.model.fetchList.called
        assert Users().getUserName.called