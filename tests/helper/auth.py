import os
import json
from flask import Flask
from bson.objectid import ObjectId
from Application.users.Models.Users import users
from Core.Factories.Database import DbFactory as db

class Auth:
  email: str = "john.doe@test.com"
  password: str = "CUtpiq@l+3#"
  organization_name = "John Doe Test Corp."
  token: str = ""
  refresh_token = ""
  remember_me: bool = False
  fingerprint: str = "9e8ce2a57b80b51f3b64c0ac64eb324c2"
  client = None
  verification_hash: str
  permissions: list = [
    "accounts~feedbacks~all~create",
    "accounts~feedbacks~all~list",
    "accounts~users~all~create",
    "accounts~users~all~invite",
    "accounts~users~all~list",
    "accounts~users~all~profile",
    "accounts~users~all~update",
    "accounts~users~all~change-password",
    "accounts~users~all~validate-password-reset-token",
    "accounts~users~all~reset-password",
    "accounts~users~all~validate-verification-hash",
    "accounts~users~all~generate-authenticator-qr",
    "accounts~users~all~activate-authenticator-app",
    "accounts~users~all~regenerate-recovery-codes",
    "accounts~users~all~disable-2fa",
    "accounts~sign-in~all~signin-as-client",
    "accounts~users~all~activate-2fa-sms",
    "accounts~users~all~get-usernames",
    "accounts~users~all~account-manager",
    "accounts~users~all~organizations",
    "accounts~users~all~manage-status",
    "accounts~users~all~manage-lock",
    "accounts~accounts~all~list",
    "accounts~accounts~all~activeusers",
    "accounts~accounts~all~overview",
    "accounts~accounts~all~manage-lock",
    "accounts~accounts~all~manage-status",
    "accounts~users~all~generate-password-reset-link",
    "accounts~users~all~change-password",
    "accounts~roles~instance~list",
    "accounts~roles~all~create",
    "accounts~roles~all~permission",
    "accounts~roles~all~update",
    "accounts~permissions~all~list",
    "accounts~permissions~all~create",
    "accounts~sign-in~all~switch",
    "accounts~sign-in~all~logout",
    "accounts~user_permissions~all~list",
    "accounts~user_permissions~all~create",
    "accounts~scopes~all~create",
    "accounts~scopes~all~list",
    "accounts~scopes~all~update",
    "accounts~app-registrations~instance~create",
    "accounts~app-registrations~instance~list"
  ]
  
  def __init__(self) -> None:
    self.header = {"Content-Type": "application/json"}
  
  def __register(self):

    #Insert the roles first
    role_doc = {
      "slug": 'account-owner-role',
      "app_slug": "accounts",
      "name": "Accounts Role",
      "permissions": self.permissions,
      "default": True
    }

    db.instance['roles'].insert_one(role_doc)

    # Inserting a hr role doc
    db.instance['roles'].insert_one({
      "slug": 'account-owner-role',
      "app_slug": "hr",
      "name": "Hr Role",
      "permissions": [
        'hr~module~scope~action'
      ],
      "default":True
    })

    # Create the signup
    payload = {
      "first_name": "John",
      "middle_name": "Middle",
      "company_name": self.organization_name,
      "last_name": "Doe",
      "middle_name": "Middle",
      "company_country": "INDIA",
      "email" : self.email,
      "password" : self.password,
      "company_country": "IN"
    }
    resp = self.client.post('/sign-up/', json=payload, headers=self.header)
    data = json.loads(resp.data)
    print('Response', data)
    if resp.status_code != 200:
      raise Exception("Registration failed")
    user = users.getCollection().find_one({
      "_id": ObjectId(data["data"]['insertedIds']['user'])
    })
    return user.get('organizations')[0].get('invitation').get('hash')
      
  
  def __verify(self, hash):
    resp = self.client.get(f'users/verify-email/{hash}')
    if resp.status_code != 200:
        raise Exception("Registration failed")

  def __login(self):
    payload = {
      "email" : self.email,
      "password" : self.password,
      "host_data": {
          "fingerprint": self.fingerprint
      }
    }
    resp = self.client.post('/sign-in/', json=payload, headers=self.header)
    if resp.status_code != 200:
      raise Exception("Login failed")
    data = json.loads(resp.data)
    return data['result']['access_token'], data['result']['refresh_token']
  
  def login(self, client):
    if self.token == "":
      for col in db.instance.list_collection_names():
        db.instance[col].drop()
      self.client = client
      hash = self.__register()
      self.__verify(hash)
      self.token, self.refresh_token = self.__login()
      # print('Refresh token', self.refresh_token)
      # print('Retrieved token', self.token)
      # db.instance.user_permissions.update_many({}, {
      #   "$set": {
      #     "permissions": self.permissions
      #   }
      # })
    return self.token

auth = Auth()