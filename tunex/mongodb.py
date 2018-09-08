#!/usr/bin/env python

from pymongo import MongoClient


class MongoDatabase:
    def __init__(self, host, port):
        self.mongoclient = None
        self.host = host
        self.port = port

    def get_user_info_from_name(self, username):
        if not self.mongoclient:
            self.mongoclient = MongoClient(self.host, self.port)

        db = self.mongoclient['dbUsersData']
        collection = db['usersData']
        cursor = collection.find({"userInfo.username": username})
        if cursor.count() == 0:
            return None
        else:
            return cursor[0]["userInfo"]

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port