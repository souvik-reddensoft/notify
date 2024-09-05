import os
import sys
import base64
import logging
import traceback
from urllib.parse import urlparse
from bson.objectid import ObjectId
from flask import Request, Response as ResponseBase, Flask
from flask.json import dumps, JSONEncoder as JSONEncoderBase
from werkzeug.exceptions import Unauthorized, NotFound, HTTPException, InternalServerError, Forbidden
import jwt
from jwt.exceptions import PyJWTError
from Core.Factories.Database import DbFactory as db
from Core.Helpers import Helper
from typing import Callable



class JSONEncoder(JSONEncoderBase):
    def default(self, o):

        if isinstance(o, ObjectId) or isinstance(o, Callable):
            return str(o)
        return super().default(o)


class Response(ResponseBase):
    default_mimetype = "application/json"


class Auth:
    exceptions = os.environ.get('ROUTE_EXCEPTIONS').split(
        '|') if 'ROUTE_EXCEPTIONS' in os.environ else ['ready']

    def __init__(self, app: Flask):
        self._app = app.wsgi_app
        app.response_class = Response
        app.json_encoder = JSONEncoder
        self.jwt_data = None

    def __call__(self, environ, start_response):

        def customResponse(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Credentials', "true"))
            headers.append(('Access-Control-Allow-Origin', req.environ.get('HTTP_ORIGIN', '*')))
            headers.append(('Access-Control-Allow-Methods',
                           "GET, POST, PATCH, PUT, DELETE, OPTIONS"))
            headers.append(('Access-Control-Allow-Headers',
                           "Origin, Content-Type, Authorization, x-api-key, X-DOMAIN"))
            return start_response(status, headers, exc_info)

        req = Request(environ)
        try:
            if '/'.join(req.path.removeprefix(os.environ.get('ROUTE_PREFIX',
                                                             '')).strip('/').split('/')[0:2]) not in self.exceptions:
                
                self.authenticate(req, environ)
                self.authorize(req, environ)

            # environ['jwt_data'] = {'token': { 'userInfo': {'id': ObjectId() } }}
            # environ['permission_data'] = [{'k': 'all'}]

            return self._app(environ, customResponse)

        except HTTPException as ex:

            resp = Response(dumps({
                'success': False,
                'message': ex.description,
                'error': {
                    'module-code': os.environ.get('SERVICE_MODULE_CODE', '') + str(ex.code if hasattr(ex, 'code') else 500),
                    'name': ex.__class__.__name__
                }
            }), status=ex.code if req.method != 'OPTIONS' else 200)
            return resp(environ, customResponse)

    def authenticate(self, request: Request, environ):
        # STAGE 1: check if Authorization is present or not
        if 'Authorization' not in request.headers:
            raise Unauthorized('Bearer Token is required')
        try:
            # STAGE 2: check if the token is verified
            token, token_data = self.verifyToken(request)

            # STAGE 3: check if token exists in the database
            # * As there is no way to invalidate a token so when a user is logged out then we are deleting it from the database.
            # * But if the user makes a request with the previous token then the above JWT method will still treat it as a valid token.
            # * So we need to check if the token also exists in the DB or not.
            client_info = self.findToken(token, token_data['userInfo']['id'])

            # STAGE 4: check company if the company matches with the

            self.jwt_data = environ['jwt_data'] = {
                'token': {
                    **token_data,
                },
                'client_info': client_info
            }
            
        except Unauthorized as ex:
            raise Unauthorized(ex.description) from ex
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()  # pylint: disable=unused-variable
            logging.error(
                ex.__class__.__name__,
                extra={
                    'json_fields': {
                        'error': ex.args[0],
                        # pylint: disable=duplicate-code
                        'http_request': {
                            'remote-address': request.remote_addr,
                            'method': request.method,
                            'url': request.url,
                            'http-version': request.environ.get('SERVER_PROTOCOL'),
                            'user-agent': request.user_agent.string,
                            'status-code': 500
                        },
                        'traceback': [
                            {
                                'file': trace.filename,
                                'line': trace.line,
                                'line_no': trace.lineno,
                                'func_name': trace.name
                            } for trace in traceback.extract_tb(exc_tb)
                        ]
                    }
                }
            )
            raise InternalServerError('Something went wrong') from ex

    def authorize(self, request: Request, environ):
        paths = request.path.removeprefix(os.environ.get(
            'ROUTE_PREFIX', '')).strip('/').split('/')
        if 'socket.io' in paths:
            return
        if len(paths) < 2:
            print("ok")
            raise NotFound()
        scopes_to_find = []
        scopes_in_order = ['all', 'owner', 'instance']
        for key in scopes_in_order:
            scopes_to_find.append(
                f"notify~{paths[0]}~{key}~{paths[1]}")
        result = list(
            db.instance['user_permissions'].aggregate(
                [
                    {
                        '$match': {
                            'permission_key': {
                                '$eq': f"{self.jwt_data['token']['userInfo']['permissionKey']}",
                            }
                        }
                    },
                    {
                        '$project': {
                            '_id': 0,
                            "permissions": {
                                "$filter": {
                                    "input": "$permissions",
                                    "as": "permission",
                                    "cond": {
                                        '$in': [
                                             "$$permission",
                                             scopes_to_find
                                        ]
                                    }
                                }
                            }
                        }
                    },
                    # {
                    #     '$match': {

                    #         'permissions': {
                    #             '$in': [paths[1]]
                    #         }
                    #     }
                    # },
                ]
            )
        )

        if len(result) == 0 or len(result[0]['permissions']) == 0:
            raise Forbidden(
                'Request couldn\'t be completed as no permission is found')

        scope = list(
            map(lambda permission: {"k": permission.split('~')[2]}, result[0]['permissions']))

        if len(scope) > 1:
            # print('Multiple scopes found', scope)
            mapped_scopes = list(
                map(lambda permission: permission.split('~')[2], result[0]['permissions']))
            # print(mapped_scopes)
            for perm in scopes_in_order:
                # perm = { "k": perm }
                if perm in mapped_scopes:
                    scope = [{"k": perm}]
                    break

        # print("selected scope", scope)
        environ['permission_data'] = scope

    def verifyToken(self, request: Request):
        token = request.headers.get('Authorization').split()[-1]
        try:
            token_data = jwt.decode(
                token,
                options={"verify_signature": False}
            )
        except PyJWTError as ex:
            raise Unauthorized(ex.__class__.__name__ +
                               ': ' + ex.args[0]) from ex

        # Decode base64 encoded ids
        token_data['userInfo']['id'] = ObjectId(
            base64.b64decode(token_data['userInfo']['id']).decode('utf-8'))

        return token, token_data

    def findToken(self, token, user_id):
        client_data = db.instance['jwt_manage'].find_one({
            'payload.jwt.token': token,
            'payload.user_id': user_id
        })

        # print(client_data)

        if client_data is None:
            raise Unauthorized('You\'re not logged in')

        return client_data

    def findAccount(self, org_id):
        organization = db.instance['organizations'].find_one(
            {"_id": ObjectId(org_id)})
        if organization is not None:
            return organization['account_id']
        return None
