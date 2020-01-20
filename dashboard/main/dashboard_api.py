# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard_api.py


from flask import request, current_app
from flask_restful import Resource, reqparse
#from flask_socketio import emit, join_room, leave_room
from . import ACTIVE_ROOMS
from .. import channel 

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
        for channel_id, channel in ACTIVE_ROOMS.items():
            if args.sid in channel.subscribed_clients:
                return_ch_list.append(channel_id)

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
        new_ch1 = channel.channel(args["ch_grp"], args["ch1_h"], args["ch1_v"])
        new_ch2 = channel.channel(args["ch_grp"], args["ch2_h"], args["ch2_v"])
        current_app.logger.info(f"In open_rooms::get: New request: ch1={new_ch1}, ch2: {new_ch2}, analysis: {args['analysis']}, sid: {args['sid']}")

        for channel_id in list(ACTIVE_ROOMS.keys()):
            loop_channel = ACTIVE_ROOMS[channel_id]
            if ((loop_channel.ch1 == new_ch1) & 
                (loop_channel.ch2 == new_ch2) & 
                (loop_channel.analysis_type == args["analysis"])):
                current_app.logger.info(f"In open_rooms::get: Channel {loop_channel.channel_id} has the requested configuration")
                return({"active_room": loop_channel.channel_id})
            else:
                current_app.logger.info(f"In open_rooms::get: Active room {channel_id} has different configuration than the one requested")

        # If we are here, there is no channel with the requested configuration.
        new_room = channel.db_update_channel(new_ch1, new_ch2, args['analysis'])
        ACTIVE_ROOMS[new_room.channel_id] = new_room
        current_app.logger.info(f"In open_rooms::get: Could not match request to a room. Created {new_room.channel_id}: {new_room}")

        return({"active_room": new_room.channel_id})


# class enter_room(Resource):
#     def __init__(self):
#         current_app.logger.info("enter_room::__init__()")
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument("sid", type=str, location="args")
#         self.parser.add_argument("room_id", type=str, location="args")

#     def put(self):
#         """Signal the client to enter a room with given id"""
#         global ACTIVE_ROOMS

#         data = json.loads(request.data)
#         current_app.logger.info(f"In create_room::post. data={data}")

#         #args = self.parser.parse_args()
#         #current_app.logger.info(f"In enter_room::put: sid: {args['sid']}, room_id: {args['room_id']}")

#         assert(data['room_id'] in ACTIVE_ROOMS.keys())

#         # Leave any other room we are currently in
#         for room_id in list(ACTIVE_ROOMS.keys()):
#             loop_room = ACTIVE_ROOMS[room_id]
#             if data['sid'] in loop_room.subscribed_clients:
#                 loop_room.remove_client(data['sid'])
#                 leave_room(room_id, sid=data['sid'])

#             if len(loop_room.subscribed_clients) == 0:
#                 ACTIVE_ROOMS.pop(room_id)

#         # Join the requested room
#         ACTIVE_ROOMS[data['room_id']].add_client(data['sid'])
#         join_room(data['room_id'], sid=data['sid'])     



# class create_room(Resource):
#     """Creates a new room on the server for the given channel configuration"""
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument("ch_grp", type=str, location="args")
#         self.parser.add_argument("ch1_h", type=int, location="args")
#         self.parser.add_argument("ch1_v", type=int, location="args")
#         self.parser.add_argument("ch2_h", type=int, location="args")
#         self.parser.add_argument("ch2_v", type=int, location="args")
#         self.parser.add_argument("analysis", type=str, location="args")
#         self.parser.add_argument("sid", type=str, location="args")


#     def get(self):
        
#         # """Create a new room for the client with the provided configuration"""
        
#         global ACTIVE_ROOMS
        

#         args = self.parser.parse_args()

#         current_app.logger.info(f"In create_room::get. args = {args}")

#         req_ch_grp = args['ch_grp']
#         new_ch1 = channel.channel(args["ch_grp"], args["ch1_h"], args["ch1_v"])
#         new_ch2 = channel.channel(args["ch_grp"], args["ch2_h"], args["ch2_v"])

#         # Leave any other room we are currently in
#         for room_id in list(ACTIVE_ROOMS.keys()):
#             loop_room = ACTIVE_ROOMS[room_id]
#             if args['sid'] in loop_room.subscribed_clients:
#                 current_app.logger.info(f"In create_room::get. Client {args['sid']} is in room {loop_room}. Leaving the room")
#                 loop_room.remove_client(args['sid'])
#                 leave_room(room_id, sid=args['sid'])
                

#             if len(loop_room.subscribed_clients) == 0:
#                 current_app.logg.info(f"In create_room::get: Room {loop_room} has no active clients. Deleting room")
#                 ACTIVE_ROOMS.pop(room_id)

#         new_room = channel.db_update_channel(new_ch1, new_ch2, args['analysis'])
#         current_app.logger.info(f"In create_room::get: Creating room id={new_room.channel_id}: {new_room}.")
        
#         #new_room.add_client(args['sid'], socketio)
#         #ACTIVE_ROOMS[new_room.channel_id] = new_room
#         #join_room(new_room.channel_id, args['sid'])

#         #current_app.logger.info(f"Exiting")

#         return({"new_room_id": new_room.channel_id})





# End of file dashboard_api.py
