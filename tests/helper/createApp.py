from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from Core.Boot.Load import Framework
from Core.Middlewares.Auth import Auth
from Core.Factories.Database import DbFactory


def createApp():
    app = Flask(__name__, static_folder=None)
    DbFactory('Mongo','instance').create()
    app.wsgi_app = Auth(app)
    Framework.run(app)

    return app