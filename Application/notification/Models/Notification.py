from os import environ
from datetime import datetime
from bson.objectid import ObjectId
from Core.Models.Model import Model as Base


class Notification(Base):
    collection = "notifications"

    fields = {
        "_id": {
            "show": True,
            "searchable": False,
            "export": False,
            "form": {"show": True, "type": "hidden", "required": True},
        },
        "message": {
            "show": True,
            "searchable": False,
            "export": True,
            "form": {"show": True, "type": "text", "required": False},
            "rules": {"type": "string", "required": False},
        },
        "app_slug": {
            "show": True,
            "searchable": True,
            "export": True,
            "form": {"show": True, "type": "text", "required": True},
            "rules": {
                "type": "string",
                "required": True,
                "allowed": environ.get("ALLOWED_APPS", "").split("|"),
            },
        },
        "read_status": {
            "type": "boolean",
            "export": True,
            "default": False,
            "allowed": [True, False]
        },
        "created_at": {
            "show": True,
            "searchable": False,
            "export": True,
            "form": {
                "show": False,
            },
        },
        "created_by": {
            "show": True,
            "searchable": False,
            "export": True,
            "form": {
                "show": False,
            },
            "rules": {"type": "object_id"},
        },
    }

    def create(self, document, token, default_data=True):
        if default_data:
            now = datetime.now()
            if not isinstance(document, list):
                document = [document]

            for doc in document:
                doc = self.typeCast(doc, True)
                if token is not None:
                    doc["created_by"] = ObjectId(token["userInfo"]["id"])

                doc["created_at"] = now
                doc["deleted_at"] = None

        return self.getCollection().insert_many(document, ordered=False).inserted_ids


notification = Notification()
