from Core.Boot.Plugin import *
from flask import request
from Application.notification.Models.Notification import notification as model
from flask_socketio import SocketIO, join_room, emit


class Notification:
    def __init__(self):
        self.model = model
        self.socketio = SocketIO() 
        self.user_rooms = {}

    

notification = Notification()
