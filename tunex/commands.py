#!/usr/bin/env python

import sys
from context import Context


class Commands:
    def __init__(self, mongodborm, userstorage):
        self.mongodbORM = mongodborm
        self.userStorage = userstorage
        self.userContext = None

    def setupUser(self, username):
        result = self.mongodbORM.get_user_info_from_name(username)
        if result is not None:
            if result["username"] and result["awssecret"] and result["awstoken"] and result["awsregion"] and result["awskeyname"]:
                self.userStorage.set_username(result["username"])
                self.userStorage.set_awssecret(result["awssecret"])
                self.userStorage.set_awstoken(result["awstoken"])
                self.userStorage.set_awsregion(result["awsregion"])
                self.userStorage.set_awspubkeyname(result["awskeyname"])
                self.userContext = Context(self.userStorage.get_awssecret(),
                                           self.userStorage.get_awstoken(),
                                           self.userStorage.get_awsregion())
                print 'User setup successful detected X running clusters'
            else:
                print 'User setup not complete in ScaleX Database'
                sys.exit(2)
        else:
            print 'User setup failed! Username not found in ScaleX Database'
            sys.exit(2)
