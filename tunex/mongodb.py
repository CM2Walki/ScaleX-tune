#!/usr/bin/env python

from pymongo import MongoClient


class MongoDatabase:
    def __init__(self, host, port):
        self.mongoclient = None
        self.host = host
        self.port = port

    def initdb(self):
        if not self.mongoclient:
            self.mongoclient = MongoClient(self.host, self.port)

    def get_user_info_from_name(self, username):
        self.initdb()
        db = self.mongoclient['dbUsersData']
        collection = db['usersData']
        cursor = collection.find({"userInfo.username": username})
        if cursor.count() == 0:
            return None
        else:
            return cursor[0]["userInfo"]

    def create_perf_data_db(self, username):
        self.initdb()
        db = self.mongoclient['dbPerfData']
        collection = None
        if "usersPerfData" in db.collection_names():
            collection = db['usersPerfData']
        else:
            collection.create_collection('usersPerfData')
        userCol = {"username": str(username), "LatencyDatapoints": [], "ResponseTimeDatapoints": []}
        collection.updateOne(userCol, upsert=True)

    def add_latency_datapoint(self, username, latency, timestamp):
        self.initdb()
        db = self.mongoclient['dbPerfData']
        collection = db['usersPerfData']
        userCol = {"username": str(username)}, {"$push": {"LatencyDatapoints": {"$each": [{"Timestamp": timestamp, "Average": latency}], "$sort": {"Timestamp": -1}, "$slice": 60}}}
        collection.update(userCol)

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port
