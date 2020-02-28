# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard_api.py


from flask import request, current_app
from flask_restful import Resource, reqparse
#from flask_socketio import emit, join_room, leave_room
from . import ACTIVE_ROOMS
from .. import room_manager 
from ..channel import channel

import json

"""Define the REST api for the dashboard.

This serves as an interface for the client to currently running rooms.

For example, a client may inquire if there is a currently open room for the
channel pairs ch_grp=L, ch1_h = 1, ch1_v=4, ch2_h=2, ch2_v=4.

To do so, the client sends an inquiry to
server/dashboard/room?ch_grp=L&ch1_h=1&ch1_v=4&ch2_h=2&ch2_v=4.

The answer is a json file with the rooms
"""


"""
Parameters:
===========
ch_grp: string, channel group. Must be in ['L', 'G', 'H']
ch1_h, int, channel1, horizontal. 1 <= ch1_h <= 24
ch1_v, int, channel1, vertical.   1 <= ch1_v <= 8
ch2_h, int, channel2, horizontal. 1 <= ch2_h <= 24
ch2_v, int, channel2, vertical.   1 <= ch2_v <= 8
"""


class subscribed_rooms(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("sid", type=str, location="args")

    def get(self):
        """Returns a list of rooms that the client currently subscribes to."""

        global ACTIVE_ROOMS

        return_ch_list = []

        args = self.parser.parse_args()
        for room_id, room in ACTIVE_ROOMS.items():
            if args.sid in room.subscribed_clients:
                return_ch_list.append(room_id)

        current_app.logger.info(f"In subscribed_rooms::get client {args.sid} is in rooms {return_ch_list}")
        return({"subscribed_rooms": return_ch_list})

class open_rooms(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ch_grp", type=str, location="args")
        self.parser.add_argument("ch1_h", type=int, location="args")
        self.parser.add_argument("ch1_v", type=int, location="args")
        self.parser.add_argument("ch2_h", type=int, location="args")
        self.parser.add_argument("ch2_v", type=int, location="args")
        self.parser.add_argument("analysis", type=str, location="args")
        self.parser.add_argument("sid", type=str, location="args")

    def get(self):
        """Searches the currently active rooms and looks for one with an identical
        configuration than the one requested."""

        global ACTIVE_ROOMS

        args = self.parser.parse_args()        
        new_ch1 = channel(args["ch_grp"], args["ch1_h"], args["ch1_v"])
        new_ch2 = channel(args["ch_grp"], args["ch2_h"], args["ch2_v"])
        current_app.logger.info(f"In open_rooms::get: New request: ch1={new_ch1}, ch2: {new_ch2}, analysis: {args['analysis']}, sid: {args['sid']}")

        for room_id in list(ACTIVE_ROOMS.keys()):
            loop_room = ACTIVE_ROOMS[room_id]
            if ((loop_room.ch1 == new_ch1) & 
                (loop_room.ch2 == new_ch2) & 
                (loop_room.analysis_type == args["analysis"])):
                current_app.logger.info(f"In open_rooms::get: Room {loop_room.room_id} has the requested configuration")
                return({"active_room": room_id.room_id})
            else:
                current_app.logger.info(f"In open_rooms::get: Active room {room_id} has different configuration than the one requested")

        # If we are here, there is no room with the requested configuration.
        new_room = room_manager.room_manager(new_ch1, new_ch2, args['analysis'])
        ACTIVE_ROOMS[new_room.room_id] = new_room
        current_app.logger.info(f"In open_rooms::get: Could not match request to a room. Created {new_room.room_id}: {new_room}")

        return({"active_room": new_room.room_id})


# End of file dashboard_api.py