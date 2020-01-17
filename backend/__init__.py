# File backend/__init__.py
# -*- Encoding: UTF-8 -*-

"""The __init__.py serves double duty: it will contain the application factory, 
and it tells Python that the flaskr directory should be treated as a package."""

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(test_config=None):
    """Creates and configures the app"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Register the dashboard blueprint in the main __init__.py:
    from .views import dashboard
    app.register_blueprint(dashboard, url_prefix="/")

    socketio.init_app(app)

    return app

# End of file __init__py