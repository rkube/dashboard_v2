# -*- Encoding: UTF-8 -*-
# File # file dashboard_v2/backend/dashboard/dashboard_events.py

from flask import session, current_app
from flask_socketio import emit, join_room, leave_room
from .. import socketio

from . import ACTIVE_ROOMS

@socketio.on("connect")
def test_connect():
    """Sent by clients when they enter a room.
    A status message "is broadcast to all people in the room."""
    #room = session.get('room')
    #join_room(room)
    current_app.logger.info(f"Client connected")
    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)

@socketio.on("leave")
def leave_room():
    """unsubscribes a client from a room"""
    current_app.logger.info(f"In leaving room")


@socketio.on("join")
def join_room(data):
    """subscribes a client to a given room"""
    current_app.logger.info(f"Joining room. data = {data}")



# End of file dashboard_events.py