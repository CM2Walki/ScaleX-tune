#!/usr/bin/env python
from pymongo import MongoClient


class MongoDatabase():
    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.host = host
        self.port = port

    def get_user_info_from_name(self, username):
        db = self.client['dbUsersData']
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