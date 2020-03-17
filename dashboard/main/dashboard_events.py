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

@socketio.on("request-leave")
def request_leave_room(data):
    """Handles leave requests from clients"""
    assert("room" in data.keys())
    assert("sid" in data.keys())

    current_app.logger.info(f"request-leave, room: {data['room']}")
    leave_room(data['room'])
    ACTIVE_ROOMS[data['room']].remove_client(data['sid'])
    
    if( len(ACTIVE_ROOMS[data['room']].subscribed_clients) == 0 ):
        current_app.logger.info(f"request-leave: deleting room {data['room']}")
        ACTIVE_ROOMS.pop(data['room'])


@socketio.on("request-join")
def requst_join_room(data):
    """Handles join requests from clients"""
    assert("room" in data.keys())
    assert("sid" in data.keys())

    current_app.logger.info(f"request-join. room: {data}")

    join_room(data['room'])
    ACTIVE_ROOMS[data['room']].add_client(data['sid'], socketio)


# End of file dashboard_events.py