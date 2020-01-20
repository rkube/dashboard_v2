# Begin file backend/views/__init__.py

from flask import Blueprint
from flask_socketio import SocketIO
from flask_restful import Api, Resource, url_for


# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
dashboard = Blueprint("dashboard", __name__, template_folder="templates")

ACTIVE_ROOMS = {}

from . import dashboard_routes, dashboard_api, dashboard_events


socketio = SocketIO()

def create_app(test_config=None):
    """Creates and configures the app"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Register the dashboard blueprint in the main __init__.py:
    from dashboard import dashboard
    api = Api(dashboard)

    #from dashboard.dashboard_api import open_rooms, enter_room, create_room, subscribed_rooms
    #api.add_resource(open_rooms, '/open_rooms')
    #api.add_resource(enter_room, '/enter_room')
    #api.add_resource(create_room, '/create_room')
    #api.add_resource(subscribed_rooms, '/subscribed_rooms')
    
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    # Start running socketio
    socketio.init_app(app)
    return app

#from . import dashboard_routes, dashboard_events, dashboard_api


# End file __init__.py