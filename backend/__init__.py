# File backend/__init__.py
# -*- Encoding: UTF-8 -*-

"""The __init__.py serves double duty: it will contain the application factory, 
and it tells Python that the flaskr directory should be treated as a package."""

from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api, Resource, url_for

socketio = SocketIO()

def create_app(test_config=None):
    """Creates and configures the app"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Register the dashboard blueprint in the main __init__.py:
    from .dashboard import dashboard
    api = Api(dashboard)

    #class TodoItem(Resource):
    #    def get(self, id):
    #        return {'task': 'Say "Hello, World!"'}

    from .dashboard.dashboard_api import open_rooms
    api.add_resource(open_rooms, '/findroom')

    app.register_blueprint(dashboard, url_prefix="/dashboard")

    # Start running socketio
    socketio.init_app(app)
    return app

# End of file __init__py