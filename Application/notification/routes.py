from flask import Blueprint
from Application.notification.Controllers.Notification import notification

notification_router = Blueprint("notification", __name__)


@notification_router.route("/create", methods=["POST"])
def send_notification():
    return notification.send_notification()