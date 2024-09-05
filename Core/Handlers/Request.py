
import json
import logging
import os
from urllib.parse import urlparse
from flask import Flask, request, abort
import i18n
from bson import ObjectId
from Core.Factories.Database import DbFactory as db
from Core.Boot.Plugin import AppPlugin
from Core.Boot.Bus import MessageBus
from Core.Helpers import Helper

class RequesHandler:
    __temp_record = {}
    @staticmethod
    def handle(app: Flask):

        @app.before_request
        def setLang():
            if 'Accept-Language' in request.headers:
                i18n.set('locale', request.headers.get('Accept-Language'))
            else:
                i18n.set('locale', 'en')
            request.t = i18n.t

        @app.after_request
        def logRequest(response):
            if (request.headers.get("HTTP-X-REAL-IP", None)):
                ip_address = request.headers.get("HTTP-X-REAL-IP")
            elif (request.headers.get("HTTP-X-Client-IP", None)):
                ip_address = request.headers.get("HTTP-X-Client-IP")
            else:
                headers_list = request.headers.get("X-Forwarded-For", None)
                ip_address = headers_list.split(",")[0] if headers_list else request.remote_addr
            
            request_info = {
                'remote-address': ip_address,
                'method': request.method,
                'url': request.url,
                'http-version': request.environ.get('SERVER_PROTOCOL'),
                'user-agent': request.user_agent.string,
            }
            # pylint: disable=logging-not-lazy,consider-using-f-string
            logging.info(
                'Request Details of %s [ %s ]: %s %s -- %s' % (
                    request_info['remote-address'],
                    request_info['user-agent'],
                    request_info['method'],
                    request_info['url'],
                    response.status_code
                ),
                extra = {
                    'json_fields': {
                        'http_request': {**request_info, **{ 'status-code': response.status_code }}
                    }
                }
            )
            if (Helper.activityLogAllowed(response)):
                MessageBus.produce('APP', 'logs_manage', {
                    'request_header' : request.headers,
                    'request_body' : request.data.decode('utf-8'),
                    'extra' : {
                        'path' : request.path,
                        'route_prefix' : os.environ.get('ROUTE_PREFIX',''),
                        'url' : request.url,
                        'method' : request.method,
                        'args' : request.args,
                        'user_agent' : request.headers['User-Agent'],
                        'remote_addr' : ip_address,
                        'status_code' : response.status_code
                    },
                    'jwt_data' : request.environ.get('jwt_data', None),
                    'response_body' : response.data.decode('utf-8'),
                    'old_record' : RequesHandler.__temp_record
                })
                RequesHandler.__temp_record = None
            return response

        @app.before_request
        def authPlugin():
            request.active_plugins = db.instance['active-plugins'].find_one({
                'domain_name': urlparse(request.base_url).hostname
            })
            if (
                request.path.startswith('/plugin/') and
                request.blueprint is not None and
                (
                    request.active_plugins is None or
                    request.blueprint not in AppPlugin.route_dict or
                    AppPlugin.route_dict[request.blueprint] not in request.active_plugins['plugins']
                )
            ):
                abort(403)

        @app.before_request
        def storeRequest():
            if ('update/' in request.url):
                __paths = request.path.removeprefix(os.environ.get('ROUTE_PREFIX','')).strip('/').split('/')
                module = __paths[0] if len(__paths) >= 1 else ''
                action = __paths[1] if len(__paths) >= 2 else ''
                doc_id = __paths[2] if len(__paths) >= 3 else ''
                if (action == 'update' and doc_id != ''):
                    record = db.instance[module].find_one({"_id" : ObjectId(doc_id)})
                    RequesHandler.__temp_record = record
