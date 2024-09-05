from flask import Flask
from Core.Boot.Load import Framework
from Core.Middlewares.Auth import Auth
from Core.Factories.Database import DbFactory
from Application.notification.Controllers.Notification import notification


DbFactory('Mongo', 'instance').create()
app = Flask(__name__)
notification.socketio.init_app(app)
app.wsgi_app = Auth(app)
Framework.run(app)

notification.initialize_notifications()

if __name__ == "__main__":
    notification.socketio.run(app, debug=True)
