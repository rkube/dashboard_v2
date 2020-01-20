# File backend/__init__.py
# -*- Encoding: UTF-8 -*-

"""The __init__.py serves double duty: it will contain the application factory, 
and it tells Python that the flaskr directory should be treated as a package."""

from flask import Flask
import eventlet
eventlet.monkey_patch()


from dashboard import create_app, socketio


if __name__ == "__main__":
    app = create_app(debug=True)
    socketio.run(app)

# End of file __init__py