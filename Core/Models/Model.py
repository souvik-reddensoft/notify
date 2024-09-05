import json
import os
from typing import List
from abc import ABC
from datetime import datetime
import pymongo
from flask import request
from werkzeug.exceptions import BadRequest
from bson.objectid import ObjectId
from Core.Factories.Database import DbFactory as db


class Model(ABC):
    custom_collection = ""
    collection: str
    fields: dict

    scopes = {
        'owner': {
            'jwt_key': 'userInfo',
            'collection_key': 'created_by'
        },
        'store': {
            'jwt_key': 'storeInfo',
            'collection_key': 'store_id'
        },
        'instance': {
            'jwt_key': 'orgInfo',
            'collection_key': 'org_id'
        },
        'account': {
            'jwt_key': 'accountInfo',
            'collection_key': 'account_id'
        },
        're-seller': {
            'jwt_key': 'resellerInfo',
            'collection_key': 'reseller_id'
        },
    }

    def setCollection(self, collection):
        self.custom_collection = collection

    def getCollection(self):
        return db.instance[self.collection] if self.custom_collection == "" else db.instance[self.custom_collection]

    def list(self, args, trash=False):
        query = self.getListQuery(args, trash)
        data = self.fetchList(query)
        return data

    def fetchList(self, query):
        query["search"] = self.appendScope(query["search"])
        if query["empty_data"]:
            data = []
        else:
            data = self.getCollection().find({"$and": query["search"]}, query["select"]).skip(
                query["skip"]).limit(query["limit"]).sort(query["sort_field"], query["sort_order"])

        count = self.getCollection().count_documents({"$and": query["search"]})
        last_page = 1
        if count / query["per_page"] > 1:
            last_page = count // query["per_page"]
            if count % query["per_page"] > 0:
                last_page += 1

        return {
            "fields": self.getFields(),
            "results": {
                "results_count": count,
                "export_limit": int(os.getenv("EXPORT_LIMIT")),
                "results": {
                    "query": query,
                    "data": list(data),
                    "count": count,
                    "current_page": query["current_page"],
                    "per_page": query["per_page"],
                    "last_page": last_page,
                    "to": count,
                    "total": count,
                },
            }
        }
    # pylint: disable=too-many-locals

    def getListQuery(self, args, trash):
        empty_data = False
        field_list = []
        if args.get('fields') is None:
            field_list = [key for key, field in self.getFields().items()
                          if field["show"]]
        else:
            field_list = args['fields'].split(",")
        fields = {field: 1 for field in field_list}
        limit = int(10 if args.get('show') is None else args['show'])
        sort_field = "created_at" if args.get('sort') is None else args['sort']
        sort_order = 1 if args.get('sort_order') == "asc" else -1
        page = 1 if args.get('page') is None else int(args["page"])
        offset = (page - 1) * limit
        query_list = []
        search_fields = self.getFields()
        if args.get("search") is not None:
            search_term = "" if args.get("search") is None else args["search"]
            search_arr = []
            for key, field in search_fields.items():
                if field.get("searchable"):
                    search_arr.append(
                        {
                            key: {
                                "$regex": search_term,
                                "$options": "i",
                            }
                        }
                    )
            if len(search_arr) > 0:
                query_list.append({"$or": search_arr})
            else:
                empty_data = True

        if empty_data is False:
            show_trash = {"deleted_at": None} if not trash else {
                "deleted_at": {"$ne": None}}
            if args.get("trash") != "true":
                query_list.append(show_trash)

            if not args.get("where_clause") is None:
                where_clause = json.loads(args["where_clause"])
                where_fields = where_clause["where_fields"]
                where_values = where_clause["where_values"]
                for index, field in enumerate(where_fields):
                    data_type = search_fields.get(field, {}).get(
                        "rules", {}).get("type", None)
                    value = self.typeRef()[data_type](
                        where_values[index]) if data_type and data_type in self.typeRef() else where_values[index]
                    query_list.append({field: value})

        return {
            "empty_data": empty_data,
            "search": query_list,
            "select": fields,
            "limit": limit,
            "skip": offset,
            "sort_field": sort_field,
            "sort_order": sort_order,
            "sort": {sort_field: sort_order},
            "current_page": page,
            "per_page": limit,
            "trash": trash
        }

    def find(self, doc_id):
        return self.getCollection().find_one({"$and": self.appendScope([{"_id": ObjectId(doc_id)}])})

    def create(self, document, token, default_data=True):
        if default_data:
            now = datetime.now()
            if not isinstance(document, list):
                document = [document]

            for doc in document:
                doc = self.typeCast(doc, True)
                if token is not None:
                    doc['created_by'] = ObjectId(token["userInfo"]["id"])

                doc['created_at'] = now
                doc['deleted_at'] = None

        return self.getCollection().insert_many(
                document, ordered=False).inserted_ids

    def update(self, doc_id, user_id, body):
        if user_id:
            body["updated_by"] = ObjectId(user_id)

        body["updated_at"] = datetime.now()

        body = self.typeCast(body)
        document = self.getCollection().find_one_and_update(
            {"$and": [{"_id": ObjectId(doc_id)}]},
            {"$set": body},
            upsert=False,
            new=True
        )
        return document

    def delete(self, doc_id, user_id):
        now = datetime.now()
        document = self.getCollection().find_one_and_update(
            {"$and": self.appendScope([{"_id": ObjectId(doc_id)}])},
            {
                "$set": {
                    "deleted_at": now,
                    "deleted_by": ObjectId(user_id)
                }
            },
            upsert=False,
            new=True
        )
        return document

    def restore(self, doc_id, user_id):
        document = self.getCollection().find_one_and_update(
            {"$and": self.appendScope([{"_id": ObjectId(doc_id)}])},
            {
                "$set": {
                    "deleted_at": None,
                    "restored_by": ObjectId(user_id)
                }
            },
            upsert=False,
            new=True
        )
        return document

    def destroy(self, doc_id):
        result = self.getCollection().delete_one(
            {"$and": self.appendScope([{"_id": ObjectId(doc_id)}])})
        return result.deleted_count

    def isDeleted(self, doc_id):
        return self.getCollection().find_one({"$and": [{"_id": ObjectId(doc_id)}, {"deleted_at": {"$ne": None}}]})

    def getFields(self):
        return self.fields

    def schema(self, keys=None) -> dict:
        return {key: value['rules'] for key, value in self.fields.items() if 'rules' in value and (keys is None or key in keys)}

    def getDataTypeKeys(self, data_type, data=None):
        return [key for key, field in self.getFields().items() if field and (data is None or key in data) and field.get("rules", {}).get("type", {}) == data_type]

    def appendScope(self, search: List):
        # request.environ['permission_data'][0]['k'] = 'owner'   #For Testing Only
        if not 'permission_data' in request.environ:
            return search

        try:
            if request.environ['permission_data'][0]['k'] != 'all':
                scope = request.environ['permission_data'][0]['k']
                if self.scopes[scope]['jwt_key'] == 'orgInfo.orgs':
                    query = {
                        "$in": request.environ['jwt_data']['token']['orgInfo']['orgs']}
                else:
                    query = request.environ['jwt_data']['token'][self.scopes[scope]
                                                                 ['jwt_key']]['id']
                search.append({
                    self.scopes[scope]['collection_key']: query
                })
            return search
        except Exception as ex:
            raise BadRequest('Unable to extract scope from JWT') from ex

    def typeRef(self):
        return {"object_id": ObjectId, "integer": self.toInt, "datetime": self.toISODate}

    def typeCast(self, data, insert=False):
        for key, field in self.getFields().items():
            if field and key in data and field.get("rules", {}).get("type", None) in list(self.typeRef()) and data[key] is not None:
                data.update({
                    key: self.typeRef()[field.get(
                        "rules", {}).get("type", {})](data[key])
                })
            elif insert is True and key not in data and key != '_id':
                data.update({
                    key: None
                })
        return data

    def toISODate(self, input_data):
        if isinstance(input_data, str):
            input_data = datetime.strptime(input_data, '%Y-%m-%d')
        else:
            for key in list(input_data.keys()):
                input_data.update(
                    {key: datetime.strptime(input_data[key], '%Y-%m-%d')})
        return input_data

    def toInt(self, input_data):
        if isinstance(input_data, (int, str)):
            input_data = int(input_data)
        else:
            for key in list(input_data.keys()):
                input_data.update({key: int(input_data[key])})
        return input_data
