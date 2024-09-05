import os
import io
import csv
from flask import request, send_file
from werkzeug.exceptions import NotFound, BadRequest
from Core.Boot.Plugin import *
from Core.Handlers.Validate import validate
from Core.Models.Model import Model

class Controller:

    model: Model

    def __init__(self):
        self.validate = validate

    @executePlugin
    def create(self):
        # The normalization and coercion are performed on the copy of the original document
        data = self.validate(request.json, self.model.schema())
        # print(self.model.schema())
        result = self.model.create(data, request.environ['jwt_data']['token'])

        return {"message": request.t(f'{self.__class__.__name__}_create_success'.lower()), "data": {
            "insertedIds": result
        }}

    @executePlugin
    def update(self, doc_id):
        if self.model.isDeleted(doc_id) is not None:
            raise NotFound("Document already deleted")
        if not isinstance(request.json, dict):
            raise BadRequest("Expecting JSON object")
        self.validate(request.json, self.model.schema(request.json.keys()))
        data = self.model.update(doc_id, request.environ['jwt_data']["token"]["userInfo"]["id"], request.json)
        if data is None:
            raise NotFound(f"Document with {doc_id} object-id does not exists")
        return {"message": request.t(f'{self.__class__.__name__}_update_success'.lower()), "data": data}

    @executePlugin
    def delete(self, doc_id):
        if self.model.isDeleted(doc_id) is not None:
            raise Exception("Document already deleted")
        data = self.model.delete(doc_id, request.environ['jwt_data']["token"]["userInfo"]["id"])
        if data is None:
            raise NotFound(f"Document with {doc_id} object-id does not exists")
        return {"message": request.t(f'{self.__class__.__name__}_delete_success'.lower()), "data": data}

    @executePlugin
    def destroy(self, doc_id):
        if self.model.find(doc_id) is None:
            raise NotFound(f"Document with {doc_id} object-id does not exists")
        data = self.model.destroy(doc_id)
        if isinstance(data, int):
            return {"message": request.t(f'{self.__class__.__name__}_destroy_success'.lower()), "data": data}

        raise Exception("Document delete failed")

    @executePlugin
    def view(self, doc_id):
        data = self.model.find(doc_id)

        if data is None:
            raise NotFound(f"Document with {doc_id} object-id does not exists")

        return {"message": request.t(f'{self.__class__.__name__}_view_success'.lower()), "data": data}

    @executePlugin
    def list(self):
        args = request.args
        data = self.model.list(args)
        return {"message": request.t(f'{self.__class__.__name__}_list_success'.lower()), "data": data}

    @executePlugin
    def trash(self):
        args = request.args
        data = self.model.list(args, trash=True)
        return {"message": request.t(f'{self.__class__.__name__}_trash_success'.lower()), "data": data}

    @executePlugin
    def restore(self, doc_id):
        if self.model.isDeleted(doc_id) is None:
            raise Exception("Document is already restored")
        data = self.model.restore(doc_id, request.environ['jwt_data']["token"]["userInfo"]["id"])
        return {"message": request.t(f'{self.__class__.__name__}_restore_success'.lower()), "data": data}

    @executePlugin
    def createView(self):
        data = []
        for field_name, field in self.model.getFields().items():
            if "form" in field and field["form"]["show"]:
                field["form"]["name"] = field_name.lower()

                data.extend(field["form"]["fields"]) if "fields" in field["form"] else data.append(field["form"])

        return {"message": request.t(f'{self.__class__.__name__}_createview_success'.lower()), "data": data}

    @executePlugin
    def export(self):
        file_name = self.model.collection

        args = {
            "show": int(request.args.get('show')) if request.args.get('show') is not None else int(os.getenv("EXPORT_LIMIT")),
            "page": int(request.args.get('page')) if request.args.get('page') is not None else 1,
            "fields": ','.join([field_name for field_name, field in self.model.getFields().items() if field.get("export") is True]),
            "trash": request.args.get("trash")
        }

        if len(list(args.get("fields"))) < 1:
            raise Exception("No data to export")

        output = self.fetchListOfDocuments(args)
        return send_file(output, f'{file_name}.csv')


    def fetchListOfDocuments(self, args):
        data = []
        output = io.StringIO()
        csv_writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        header = []
        response = io.BytesIO()
        for field_name, field in self.model.getFields().items():
            if field.get("export") is True:
                header.append(field_name)

        csv_writer.writerow(header)
        list_of_documents = self.model.list(args)
        # print(list_of_documents)
        for data in list_of_documents.get("results").get("results").get("data"):
            row = []
            for field_name, field in self.model.getFields().items():
                if field.get("export") is True:
                    if field_name in data:
                        row.append(data[field_name])
                    else:
                        row.append('')
            csv_writer.writerow(row)

        response.write(output.getvalue().encode())
        response.seek(0)
        output.close()
        return response