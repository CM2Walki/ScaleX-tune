#!/usr/bin/env python

import namesgenerator # clustername = str(namesgenerator.get_random_name()).replace("_", "")
from context import Context


class DaemonCommands:
    def __init__(self, mongodborm, userstorage):
        self.mongodbORM = mongodborm
        self.userStorage = userstorage
        self.userContext = None

    def setup_user(self, username):
        # Try to find the user in the ScaleX database
        result = self.mongodbORM.get_user_info_from_name(username)
        if result is not None:
            # Check if we have the fields we need
            if result["username"] and result["awssecret"] and result["awstoken"] and result["awsregion"] and result["awskeyname"]:
                # Setup user
                self.userStorage.set_username(result["username"])
                self.userStorage.set_awssecret(result["awssecret"])
                self.userStorage.set_awstoken(result["awstoken"])
                self.userStorage.set_awsregion(result["awsregion"])
                self.userStorage.set_awspubkeyname(result["awskeyname"])
                # Setup AWS connection and available resources
                self.userContext = Context(self.userStorage.get_awssecret(),
                                           self.userStorage.get_awstoken(),
                                           self.userStorage.get_awsregion())
                # Retrieve running clusters
                return result
                response = self.userContext.build_context(self.userStorage)
                return response
            else:
                return 'User setup not complete in ScaleX Database!\nMake sure the fields username, ' \
                       'awssecret, awstoken, awsregion and awskeyname are setup for user %s' % username
        else:
            return 'User setup failed! Username not found in ScaleX Database'

    def cluster_status(self):
        return "TODO"

    def cluster_run(self):
        return "TODO"

    def cluster_remove(self):
        return "TODO"

    def cluster_change(self):
        return "TODO"

    def get_active_user(self):
        result = self.userStorage.get_username()
        if result:
            return result
        else:
            return "False"
