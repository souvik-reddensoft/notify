from flask import Blueprint, jsonify

custom_route_router = Blueprint('custom', __name__)


@custom_route_router.route('/list', methods=['GET'])
def listing():
    return jsonify({
        'data': 'This is a custom List'
    })