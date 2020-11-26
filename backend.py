# File backend/__init__.py
# -*- Encoding: UTF-8 -*-

"""The __init__.py serves double duty: it will contain the application factory, 
and it tells Python that the flaskr directory should be treated as a package."""

from flask import Flask
import eventlet
eventlet.monkey_patch()

from dashboard import create_app, socketio
app = create_app(debug=True)

if __name__ == "__main__":    
    socketio.run(app)#, host="0.0.0.0")
# End of file backend.py
