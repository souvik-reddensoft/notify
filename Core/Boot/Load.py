import os
import urllib.parse
import importlib
import i18n
from flask import Blueprint, Flask
import Core.Boot.Log # pylint: disable=unused-import
from Core.Boot.Plugin import AppPlugin
from Core.Handlers.Request import RequesHandler
from Core.Handlers.Error import ErrorHandler
from Core.Boot.Bus import MessageBus
from pymongo import MongoClient
from pymongo import MongoClient
from werkzeug.exceptions import InternalServerError


class Framework:

    @staticmethod
    def run(app: Flask):
        app.register_error_handler(Exception, ErrorHandler.handle)
        app.handle_exception = ErrorHandler.handle
        RequesHandler.handle(app)
        MessageBus.load(['APP', 'AUTH'])
        AppPlugin.handle(app)

        i18n.set('filename_format', '{locale}.{format}')
        i18n.set('file_format', 'json')
        def healthCheck():
            try:
                res = None
                mongo_uri = os.getenv("MONGO_CONNECTION_TEST_URI") if os.getenv("FLASK_ENV") == "test" else os.getenv("MONGO_CONNECTION_URI")
                mongo_user = os.getenv("MONGO_TEST_USER") if os.getenv("FLASK_ENV") == "test" else os.getenv("MONGO_USER")
                mongo_password = os.getenv("MONGO_TEST_PASSWORD") if os.getenv("FLASK_ENV") == "test" else os.getenv("MONGO_PASSWORD")
                username = urllib.parse.quote(mongo_user)
                password = urllib.parse.quote(mongo_password)
                client = MongoClient(mongo_uri % (username, password))
                response = client.server_info()
                res = {"message":"Details fetched successfully!","success":True,"result":{"database":"up","version":response["version"]}}
            except Exception:
                raise InternalServerError("Connection Error!")

            return res
        app.add_url_rule("/ready","ready", lambda: {'status': True})
        app.add_url_rule("/health-check","health-check", healthCheck)
        for folder in ['Application', 'Plugins']:
            path = os.path.abspath(os.curdir) + f'/{folder}'
            modules = os.scandir(path)
            for module in modules:
                lang = path + '/' + module.name + '/Locales/lang'
                route = path + '/' + module.name + '/routes.py'
                if os.path.isdir(lang):
                    i18n.load_path.append(lang)
                if os.path.isfile(route):
                    module_router: Blueprint = getattr(
                        importlib.import_module(f'{folder}.{module.name}.routes'),
                        module.name + '_router'
                    )
                    if folder == 'Plugins':
                        AppPlugin.route_dict[module_router.name] = module.name
                        app.register_blueprint(
                            module_router, url_prefix=f'{os.environ.get("ROUTE_PREFIX", "")}/plugin/{module_router.name}'
                        )
                    else:
                        app.register_blueprint(
                            module_router, url_prefix=f'{os.environ.get("ROUTE_PREFIX", "") + "/" + module_router.name}'
                        )

        i18n.set('fallback', 'en')
