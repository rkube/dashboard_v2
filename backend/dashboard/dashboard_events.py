# -*- Encoding: UTF-8 -*-
# File # file dashboard_v2/backend/views/dashboard_events.py

from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio

@socketio.on('ping')
def joined(message):
    """Sent by clients when they enter a room.
    A status message "is broadcast to all people in the room."""
    #room = session.get('room')
    #join_room(room)
    print("Got pinged")
    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)

# End of file dashboard_events.py