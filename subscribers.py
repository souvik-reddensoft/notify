from typing import Dict, Callable
from bson.objectid import ObjectId
from dateutil import parser
from Core.Factories.Database import DbFactory as db, Collection
from json import dumps


class AppEvent:
    actions: Dict[str, Callable[[Collection, dict], bool]] = {
        'create': lambda collection, value, **kwargs: collection.insert_one(value),
        'update': lambda collection, filter, update = {}, upsert = False, **kwargs: collection.update_one(filter,{"$set" : update}, upsert=upsert),
        'delete': lambda collection, filter, **kwargs: collection.delete_one(filter)
    }

    @classmethod
    def quickstartEvents(cls, value: dict):
        db.instance['app-event'].insert_one(value)

    @classmethod
    def userManage(cls, value):
        print(dumps(value['payload'], default=str), "Logging from user_manage")
        
        try:
            value.get('payload',{}).pop('previous_info', None)
            if value['action'] == 'force-delete':
                db.instance['users'].delete_one({'_id': ObjectId(value['payload']['_id'])})
            elif value['action'] == 'create':
                db.instance['users'].insert_one(value['payload'])
            else:
                db.instance['users'].update_one(
                    {'_id': ObjectId(value['payload']['_id'])},
                    {
                    '$set': { 'is_confirm':  True}
                    }
                )
                
        except Exception as ex:
            pass
        # Todo for delete

    def __sanitizeUserManageData(self, value, user_org_list):
        org_list = [str(org['id']) for org in user_org_list]
        user_active_org_count = len(list(set(org_list)))
        if user_active_org_count > 1:
            for field in ["first_name", "middle_name", "last_name", "phone", "image"]:
                value['payload'].pop(field, "") 
        return value
    
    @classmethod
    def userPermissionsManage(cls, value):
        if '_id' in value['payload']:
            del value['payload']['_id']

        if value['action'] == 'force-delete':
            db.instance['user_permissions'].delete_one(
                {'permission_key': value['payload']['permission_key']})
        else:
            # For create and update
            db.instance['user_permissions'].update_one({'permission_key': value['payload']['permission_key']}, {
                '$set': value['payload'],
            }, upsert=True)
  

    @classmethod
    def jwtManage(cls, value):
        if '_id' in value['payload']:
            value['payload']['_id'] = ObjectId(value['payload']['_id'])

        action = value['action']
        if action == 'delete':
            db.instance['jwt_manage'].delete_one(
                {"_id": value['payload']['_id']})
        else:
            # For create and update
            db.instance['jwt_manage'].update_one({'_id': value['payload']['_id']}, {
                '$set': value['payload'],
            }, upsert=True)