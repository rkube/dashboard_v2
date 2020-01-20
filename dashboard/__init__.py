# Begin file dashboard/__init__.py
# -*- Encoding: UTF-8 -*-

from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api

socketio = SocketIO()

def create_app(debug=False):
    """Creates and configures the app"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Register the dashboard blueprint in the main __init__.py:
    from .main import dashboard
    from .main.dashboard_api import test_route, subscribed_rooms, open_rooms

    api = Api(dashboard)
    api.add_resource(test_route, "/test_route")

    api.add_resource(open_rooms, '/open_rooms')
    #api.add_resource(enter_room, '/enter_room')
    #api.add_resource(create_room, '/create_room')
    api.add_resource(subscribed_rooms, '/subscribed_rooms')
    
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    # Start running socketio
    socketio.init_app(app)
    return app


# End file __init__.py