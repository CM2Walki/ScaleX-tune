#!/usr/bin/env python
from pymongo import MongoClient


class MongoDatabase():
    def __init__(self, host, port):
        self.client = MongoClient(host, port)

    def getUserInfoFromName(self, username):
        db = self.client['dbUsersData']
        collection = db['usersData']

        cursor = collection.find({"userInfo.username": username})
        if cursor.count() == 0:
            return 0
        else:
            return cursor[0]["userInfo"]["username"]