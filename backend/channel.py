# -*- Endocing: UTF-8 -*-

import random
import string

from threading import Thread
import numpy as np



class InterruptibleThread:
    """Define an interruptible thread that is gathering data for an db_update_channel"""
    def __init__(self, socketio):
        self._running = True
        self.socketio = socketio

    def terminate(self):
        self._running = False

    def check_db_for_updates(self, room_name):
        """This process runs in the background and checks the DB for updates"""
            # Open a change stream on the data collection.
        # https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.watch

        #for _ in range(50):
        while self._running:  
            self.socketio.sleep(seconds=1.0) 
            print(f"Creating random channel data for room {room_name}")

            #data = np.random.normal(0.0, 1.0, size=(128,))
            data = np.random.randint(0, 100, size=(128,))
            self.socketio.emit("new_data", {"data": data.tolist()}, room=room_name)

        print("--- InterruptibleThread: Exiting")


class channel:
    """Simple ECEI channel model."""
    def __init__(self, ch_g, ch_h, ch_v):
        self.ch_g = ch_g
        self.ch_h = ch_h
        self.ch_v = ch_v

    def __eq__(self, other):
        return((self.ch_g == other.ch_g) & (self.ch_h == other.ch_h) & (self.ch_v == other.ch_v))

    def __repr__(self):
        return f"{self.ch_g}{self.ch_h:02d}{self.ch_v:02d}"



class db_update_channel():
    """Decsribes the configuration of a given room. Roughly this here:
    http://timmyreilly.azurewebsites.net/flask-socketio-and-more/
    """
    def __init__(self, ch1, ch2, analysis_type):
        self.ch1 = ch1
        self.ch2 = ch2
        self.analysis_type = analysis_type
        # Unique channel ID for this channel pair and type of analysis
        self.channel_id = self.generate_channel_id() 
        self.subscribed_clients = []
        self.thread = None

    def __eq__(self, other):
        return((self.ch1 == other.ch1) & (self.ch2 == other.ch2) & (self.analysis_type == other.analysis_type))

    def __repr__(self):
        print_str = f"Update channel object. ch1 = {self.ch1}, ch2 = {self.ch2}, analysis = {self.analysis_type}"
        for client in self.subscribed_clients:
            print_str += f"\n connected clients:"
            print_str += f"\n    {client}"
        return(print_str)

    def add_client(self, client_sid, socketio):
        """Subscribes a new client to this channel."""
        print(f"--- db_update_channel.add_client: adding client {client_sid}")
        #if len(self.subscribed_clients) == 0:
        #    self.thread = InterruptibleThread(socketio)
        #    socketio.start_background_task(self.thread.check_db_for_updates, self.channel_id)

        self.subscribed_clients.append(client_sid)  

    def remove_client(self, client_sid):
        """Removes a client from the subscribed list. Stops the worker thread
        if this was the last client."""
        print(f"--- db_update_channel.remove_client: removing client {client_sid}")
        self.subscribed_clients.remove(client_sid)

        if len(self.subscribed_clients) == 0:
            None
            #self.thread._running = False

    @classmethod
    def generate_channel_id(cls):
    
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