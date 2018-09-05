#!/usr/bin/env python


class Commands():
    def __init__(self, mongodbORM, userStorage):
        self.mongodbORM = mongodbORM
        self.userStorage = userStorage

    def setupUser(self, username):
        result = self.mongodbORM.get_user_info_from_name(username)
        if result:
            self.userStorage.set_username(result["username"])
            self.userStorage.set_awssecret(result["awssecret"])
            self.userStorage.set_awstoken(result["awstoken"])
            self.userStorage.set_awsregion(result["awsregion"])
            self.userStorage.set_awspubkeyname(result["awskeyname"])
        print self.userStorage.set_awssecret
