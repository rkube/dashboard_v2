# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard_api.py


from flask_restful import Resource, reqparse
from . import ACTIVE_ROOMS

"""Define the REST api for the dashboard.

This serves as an interface for the client to currently running rooms.

For example, a client may inquire if there is a currently open room for the
channel pairs ch_grp=L, ch1_h = 1, ch1_v=4, ch2_h=2, ch2_v=4.

To do so, the client sends an inquiry to
server/dashboard/room?ch_grp=L&ch1_h=1&ch1_v=4&ch2_h=2&ch2_v=4.

The answer is a json file with the rooms
"""


parser = reqparse.RequestParser()
parser.add_argument('ch_grp', type=str, location='args')
parser.add_argument('ch1_h', type=int, location='args')
parser.add_argument('ch1_v', type=int, location='args')
parser.add_argument('ch2_h', type=int, location='args')
parser.add_argument('ch2_v', type=int, location='args')


class open_rooms(Resource):
    def get(self):
        args = parser.parse_args()
        print("--- args is ", args)
        return {'task': 'Say "Hello, World!"'}

    def put(self):
        print("TodoItem: put")

        args = parser.parse_args()
        print("--- args is ", args)


# End of file dashboard_api.py
