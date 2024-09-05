import os
import re
import json
import pendulum
from flask import request
from Core.Boot.Bus import MessageBus
import random
import string
import base64
from Core.Factories.Database import DbFactory as db

class Helper:

    @staticmethod
    def encodeB64String(message: str):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    @staticmethod
    def getConfiguration(path):
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, path)
        with open(filename, 'r', encoding='utf8') as json_data_file:
            return json.load(json_data_file)

    @staticmethod
    def toLower(value):
        return value.lower()

    @staticmethod
    def toUpper(value):
        return value.upper()

    @staticmethod
    def sanitizeString(data):
        return re.sub('[^A-Za-z0-9]+', '', data)

    @staticmethod
    def resetKeys(keys, dictionary):
        for key in keys:
            if key in dictionary:
                del dictionary[key]
        return dictionary

    @staticmethod
    def convertDateToIsoDate(date_string):
        return pendulum.parse(date_string, strict=False)

    @staticmethod
    def generateSlug(s: str):
        s = s.lower().strip()
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'[\s_-]+', '-', s)
        s = re.sub(r'^-+|-+$', '', s)
        # rand_str = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
        #                    for i in range(8))
        # return s+'-'+rand_str
        return s
    
    # This function takes 3 arguments. The collection parameter is the name of the collection for which we want to add
    # autoincremented field, field is the name of the key in that collection which will hold the autoincremented value
    # and data is the payload after validation.
    @staticmethod
    def implementAutoIncrement(collection: str, field: str, data: dict | list):
        
        def updateAutoIncrementValue(collection: str, count: int) -> dict:
            document = db.instance["autoincrements"].update_one({"collection": collection}, {"$inc": {"value": count}}, upsert=True)
            return {"upsertedId": document.upserted_id if document.upserted_id is not None else "", "modified": document.modified_count}

        document = db.instance["autoincrements"].find_one({"collection": collection})
        res = {}
        if isinstance(data, dict):
            data[field] = (document["value"] + 1) if document is not None else 1
            updateAutoIncrementValue(collection, 1)
            res = data
        if isinstance(data, list):
            _list = []
            for i, doc in enumerate(data):
                doc[field] = (document["value"] + i+1) if document is not None else i+1
                _list.append(doc)
            updateAutoIncrementValue(collection, len(_list))
            res = _list
        return res

    @staticmethod
    def generateRandomString(string_type: str, length: int, lower: bool = False) -> str:
        if string_type == "digits":
            return ''.join(random.choices(string.digits, k=length))
        if string_type == "alphanumeric":
            if lower:
                return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return ''.join(random.choices(string.ascii_letters, k=length))


    @staticmethod
    def produceToKafka(action: str, topic_name, payload):
        client_info = {"initiator_service": os.environ.get('SERVICE_MODULE_CODE', 'AUTH')}
        if request:
            client_info['ua'] = request.headers.get('User-Agent')
            client_info['ip'] = request.remote_addr
            # if 'jwt_data' in request.environ:
            #     print("Headerrrrr", request.headers)
            #     client_info['jwt'] = request.headers.get('Authorization').split(' ')[1]

        payload = {
            "client_info" : client_info,
            "action" : action,
            "payload": payload
        }
        print("Topic", topic_name)
        MessageBus.produce('APP', topic_name, payload)
    
    @staticmethod
    def activityLogAllowed(response):
        excluded_urls = [
            "sign-in/validate",
            "ready"
        ]
        __paths = request.path.removeprefix(os.environ.get('ROUTE_PREFIX', '')).strip('/').split('/')
        module = __paths[0] if len(__paths) >= 1 else None
        action = __paths[1] if len(__paths) >= 2 else None

        if(bool(str(os.environ.get('ACTIVITY_LOGGER','false')).title()) is False):
            return False
        for __ex_url in excluded_urls:
            if(__ex_url in request.url):
                return False
        if(action in ["list", "create", "update", "delete", "restore"] or module in ["sign-in"]):
            return True
        if response.status_code not in [200, 202]:
            return False
        return True