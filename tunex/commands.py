#!/usr/bin/env python

import sys


class Commands:
    def __init__(self, mongodborm, userstorage):
        self.mongodbORM = mongodborm
        self.userStorage = userstorage

    def setupUser(self, username):
        result = self.mongodbORM.get_user_info_from_name(username)
        if result is not None:
            self.userStorage.set_username(result["username"])
            self.userStorage.set_awssecret(result["awssecret"])
            self.userStorage.set_awstoken(result["awstoken"])
            self.userStorage.set_awsregion(result["awsregion"])
            self.userStorage.set_awspubkeyname(result["awskeyname"])
        else:
            print 'User setup failed! Username not found in Database'
            sys.exit(2)

        # Reset context
