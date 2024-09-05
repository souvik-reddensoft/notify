import os
import json
from bson.objectid import ObjectId
from tests.helper.client import Client

def getObjectId(data):
    return data["data"]["insertedIds"][0]

class Request():
    def __init__(self, client, base_url, model, token = None, payload = None):
        # pylint:disable=R0913
        self.resp = None
        self.data = None
        self.pay_load = payload
        self.object_id = None
        self.client = Client(client)
        self.status_code = None
        self.base_url = base_url
        self.model = model
        self.token = token
        self.header = {'Authorization': f'Bearer {self.token}', "Content-Type": "application/json"}

    def create(self, empty_payload = False, fetch_object_id_fn = getObjectId):
        payload = {} if empty_payload else  self.pay_load
        self.resp = self.client["post"](f'{self.base_url}/create', json=payload, headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        self.object_id = None if empty_payload else fetch_object_id_fn(self.data)
        return self

    def update(self, payload = None):
        object_id = "6257aacf8d78d977dd640585" if self.object_id is None else self.object_id
        payload = {} if payload is None else payload
        self.resp = self.client["post"](f'{self.base_url}/update/{object_id}', json=payload, headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def list(self):
        self.resp = self.client["get"](f'{self.base_url}/list', headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def view(self):
        object_id = "6257aacf8d78d977dd640585" if self.object_id is None else self.object_id
        self.resp = self.client["get"](f'{self.base_url}/view/{object_id}', headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def delete(self):
        object_id = "6257aacf8d78d977dd640585" if self.object_id is None else self.object_id
        self.resp = self.client["post"](f'{self.base_url}/delete/{object_id}', headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def restore(self):
        object_id = "6257aacf8d78d977dd640585" if self.object_id is None else self.object_id
        self.resp = self.client["post"](f'{self.base_url}/restore/{object_id}', headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def trash(self):
        self.resp = self.client["get"](f'{self.base_url}/trash', headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def destroy(self):
        object_id = "6257aacf8d78d977dd640585" if self.object_id is None else self.object_id
        self.resp = self.client["delete"](f'{self.base_url}/destroy/{object_id}', headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def custom(self, url = "", http_method = "get", payload = None):
        self.resp = self.client[http_method](f'{self.base_url}/{url}', json=payload, headers=self.header)
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def no_jwt_custom(self, url, http_method = "get", payload = None):
        self.resp = self.client[http_method](f'{self.base_url}/{url}', json=payload, headers = {"Content-Type": "application/json"})
        self.status_code = self.resp.status_code
        self.data = json.loads(self.resp.data)
        return self

    def countDocuments(self):
        return self.model.getCollection().count_documents({})

    def getSingleSpecificData(self, query):
        return self.model.getCollection().find_one(query)

    def lastCreated(self):
        return self.model.getCollection().find_one({"_id": ObjectId(self.object_id)})
