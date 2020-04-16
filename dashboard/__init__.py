# Begin file dashboard/__init__.py
# -*- Encoding: UTF-8 -*-

from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api
import logging


socketio = SocketIO()
def create_app(debug=False):
    """Creates and configures the app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
 
    # Register the dashboard blueprint in the main __init__.py:
    from .main import dashboard
    from .main.dashboard_api import subscribed_rooms, open_rooms

    api = Api(dashboard)
    api.add_resource(open_rooms, '/open_rooms')
    api.add_resource(subscribed_rooms, '/subscribed_rooms')
    
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    logging.info(f"Available loggers: {loggers}")
    print(f"Let's go!. Available loggers: {loggers}")
    logger_sio = logging.getLogger("socketio")
    logger_sio.setLevel("WARN")
    logger_eio = logging.getLogger("engineio")
    logger_eio.setLevel("WARN")

    # Start running socketio
    socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
    return app

# End file __init__.py