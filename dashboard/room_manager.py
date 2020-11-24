# -*- Endocing: UTF-8 -*-

import os
from threading import Thread

import random
import string

import numpy as np
import pickle
from pymongo import MongoClient
import gridfs

from .channel import channel, channel_pair

def mongo_query(fs, mongo_coll, mongo_filter):
    """Queries analysis results from mongodb gridfs

    Input:
    ------
    fs, gridfs.GridFS: Link to the gridfs instance we are querying
    mongo_coll, pymongo.collection.Collection: Collection to be queired
    mongo_filter, dict: Filter used to query
    ch_idx, int: Index of gridfs array to return

    Returns:
    --------
    anl_result, ndarray: Result of the analysis
    """

    anl_entry = mongo_coll.find_one(mongo_filter)
    gridfs_id = anl_entry['result_gridfs']
    res = fs.get(gridfs_id)
    gridfs_data = res.read()
    t1 = pickle.loads(gridfs_data)

    return t1


class InterruptibleThread:
    """Define an interruptible thread that is gathering data for an db_update_channel"""
    def __init__(self, socketio):
        self._running = True
        self.socketio = socketio

    def terminate(self):
        self._running = False

    def check_db_for_updates(self, fs, mongo_coll, mongo_filter, ch_idx, room_id):
        """This process runs in the background and checks the DB for updates"""
        # Open a change stream on the data collection.
        # https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.watch

        # Get max time index where that we have data for:
        max_idx = mongo_coll.count_documents({"analysis_name": mongo_filter["analysis_name"],
                                              "description": "analysis results",
                                              "tidx": {"$gt": 0}})
        # for tidx in range(max_idx):
        #     self.socketio.sleep(seconds=0.02) 
        #     print(f"Querying mongo {tidx}/{max_idx}")
        #     mongo_filter.update({"tidx": tidx})
        #     print(f"mongo_filter = {mongo_filter}")
        #     # Find the entry for the current time index
        #     anl_entry = mongo_coll.find_one(mongo_filter)
        #     # Extract the link to the gridfs file
        #     gridfs_id = anl_entry['result_gridfs']
        #     # Extract file from gridfs
        #     res = fs.get(gridfs_id)
        #     gridfs_data = res.read()
        #     t1 = pickle.loads(gridfs_data)
        #     # Get selected channel index
        #     data = t1[ch_idx, :]
        #     # Push data to web-client
        #     self.socketio.emit("new_data", {"data": data.tolist()}, room=room_id)

        print("Entering check_db_for_updates: ", mongo_coll)
        with mongo_coll.watch() as stream:
            for item in stream:
                print(f"Got an item: _id={item['fullDocument']['_id']}")
                try:
                    gridfs_id = item['fullDocument']['result_gridfs']
                except: 
                    print("Could not access gridfs_id")
                    continue

                res = fs.get(gridfs_id)
                gridfs_data = res.read()
                t1 = pickle.loads(gridfs_data)
                data = t1[ch_idx, :]

                self.socketio.emit("new_data", {"data": data.tolist()}, room=room_id)

        # while self._running:  
        #     self.socketio.sleep(seconds=1.0) 
        #     print(f"Creating random channel NEWTHINGS!!! data for room {room_id}")

            
        #     data = np.random.randint(0, 100, size=(128,))
        #     self.socketio.emit("new_data", {"data": data.tolist()}, room=room_id)

        print("--- InterruptibleThread: Exiting")  


class room_manager():
    """Decsribes the configuration of a given room. Roughly this here:
    http://timmyreilly.azurewebsites.net/flask-socketio-and-more/
    """
    def __init__(self, ch1, ch2, analysis_type):
        self.ch1 = ch1
        self.ch2 = ch2
        self.analysis_type = analysis_type
        # Unique channel ID for this channel pair and type of analysis
        self.room_id = self.generate_room_id() 
        self.subscribed_clients = []
        self.thread = None

        with open("mongo_secret", "r") as df:
            lines = df.readlines()
        mongo_uri = lines[0].strip()
        mongo_user = lines[1].strip()
        mongo_pass = lines[2].strip()
        mongo_collection = lines[3].strip()

        #print(f"__{mongo_user}__, __{mongo_pass}__")
        client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass)
        self.db = client.get_database()
        self.coll = self.db[mongo_collection]
        # Get the channel serialization for the analysis
        res = self.coll.find_one({"description": "metadata", "analysis": self.analysis_type})
        target_pair = channel_pair(self.ch1, self.ch2)

        channel_ser = res['channel_serialization'][0]
        for chpair_idx, cp_serial in enumerate(channel_ser):
            channel1 = channel(cp_serial['ch1']['dev'], cp_serial['ch1']['ch_v'], cp_serial['ch1']['ch_h'])
            channel2 = channel(cp_serial['ch2']['dev'], cp_serial['ch2']['ch_v'], cp_serial['ch2']['ch_h'])
    
            if (channel_pair(channel1, channel2) == target_pair):
                print(f"Found target pair with index {chpair_idx}")

        self.chpair_idx = chpair_idx

        # mongo_filter defines what the room pulls out of the change stream
        self.mongo_filter = {"analysis_name": self.analysis_type, "description": "analysis results"}
        self.fs = gridfs.GridFS(self.db)


    def __eq__(self, other):
        return((self.ch1 == other.ch1) & (self.ch2 == other.ch2) & (self.analysis_type == other.analysis_type))

    def __repr__(self):
        print_str = f"Manage room object. ch1 = {self.ch1}, ch2 = {self.ch2}, analysis = {self.analysis_type}"
        for client in self.subscribed_clients:
            print_str += f"\n connected clients:"
            print_str += f"\n    {client}"
        return(print_str)

    def add_client(self, client_sid, socketio):
        """Adds the clients session_id to this room."""
        print(f"--- manage_room.add_client: adding client {client_sid} to {self.room_id}")
        if len(self.subscribed_clients) == 0:
            self.thread = InterruptibleThread(socketio)
            socketio.start_background_task(self.thread.check_db_for_updates, self.fs, self.coll, self.mongo_filter, self.chpair_idx, self.room_id)

        self.subscribed_clients.append(client_sid)  

    def remove_client(self, client_sid):
        """Removes a client from the subscribed list. Stops the worker thread
        if this was the last client."""
        print(f"--- manage_room.remove_client: removing client {client_sid} from {self.room_id}")
        self.subscribed_clients.remove(client_sid)

        if len(self.subscribed_clients) == 0:
            print(f"--- manage_room.remove_client: room is empty. Stopping thread")
            self.thread._running = False

    @classmethod
    def generate_room_id(cls):
        """Generates a random 5 digit ID"""
        id_length = 5
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase) for _ in range(id_length))


    # db = mongo_client["delta-fusion"]
    # with db.test_analysis.watch() as stream:  
    #     for change in stream: 
    #         print("change in mongo_update_stream: id = ", change)
    #         print()

    #         doc = db.data.find_one({"_id": change["documentKey"]["_id"]})

    #         # TODO:
    #         # If one of the UPDATE_CHANNELS is requesting updates on the current update,
    #         # emit it
    #         for db_channel in UPDATE_CHANNELS:
    #             if db_channel == change_of_this_channel:
    #                 #


# end of file channel.py