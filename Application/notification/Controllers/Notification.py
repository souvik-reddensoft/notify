from Core.Boot.Plugin import *
from flask import request
from Core.Controllers.Controller import Controller as Base
from Application.notification.Models.Notification import notification as model
from flask_socketio import SocketIO, join_room, emit
import json


class Notification(Base):
    def __init__(self, app=None):
        super().__init__()
        self.model = model
        self.socketio = SocketIO()
        self.user_rooms = {}

        if app is not None:
            self.socketio.init_app(app)

    def initialize_notifications(self):
        """ Attach event handlers to socketio """
        self.socketio.on_event("connect", self.handle_connect)
        self.socketio.on_event("disconnect", self.handle_disconnect)

    def handle_connect(self):
        user_id = str(request.environ["jwt_data"]["token"]["userInfo"]["id"])
        if user_id:
            self.user_rooms[user_id] = request.sid
            join_room(self.user_rooms[user_id])
            # print(f"User {user_id} connected with session ID {request.sid}")

    def handle_disconnect(self):
        user_id = str(request.environ["jwt_data"]["token"]["userInfo"]["id"])
        if user_id and user_id in self.user_rooms:
            del self.user_rooms[user_id]
            print(f"User {user_id} disconnected")


    def send_notification(self):
        data = self.validate(request.json, self.model.schema())
        user_id = str(request.environ["jwt_data"]["token"]["userInfo"]["id"])
        if user_id in self.user_rooms:
            data["read_status"] = False
            self.socketio.emit("new_notification", data, room=self.user_rooms[user_id])
            result = self.model.create(data, request.environ["jwt_data"]["token"])
            res_data = {"insertedIds": result}
            return {"message": request.t(f'{self.__class__.__name__}_create_success'.lower()), "data": json.loads(json.dumps(res_data, default=str))}
        else:
            return {"message": "User not connected"}, 400


notification = Notification()
