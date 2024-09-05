from bson.objectid import ObjectId
from flask import request
from cerberus import Validator
from cerberus.errors import BasicErrorHandler
from cerberus.validator import BareValidator
from werkzeug.exceptions import BadRequest

class AppValidator(Validator):
    def __init__(self, *args, **kwargs):
        if 'error_handler' in kwargs:
            del kwargs['error_handler']
        super().__init__(error_handler=CustomErrorHandler, *args, **kwargs)

    # pylint: disable=invalid-name
    def _validate_type_object_id(self, value):
        return ObjectId.is_valid(value)


# pylint: disable=abstract-method
class CustomErrorHandler(BasicErrorHandler):
    def _format_message(self, field, error) -> str:
        return request.t(f'validate.{error.code}', default=self.messages[error.code]).format(
            *error.info,
            constraint=error.constraint,
            field=str(field).title(),
            value=error.value
        )

def validate(data: dict | list, schema: dict, validator: BareValidator = AppValidator()) -> dict | list:
    if not data:
        raise BadRequest(request.t('request.empty_body'))

    if isinstance(data, dict):
        validator.validate(data, schema, normalize=True)
    else:
        validator.validate({'list_data': data}, {
            'list_data': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': schema
                }
            }
        }, normalize=True)

    if validator.errors:
        ex = BadRequest('Validation Error')
        ex.errors = validator.errors
        raise ex

    return validator.document['list_data'] if 'list_data' in validator.document else validator.document