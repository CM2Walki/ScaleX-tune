#!/usr/bin/env python


class Storage:
    def __init__(self):
        self.username = None
        self.awssecret = None
        self.awstoken = None
        self.awsregion = None
        self.awspubkeyname = None
        self.awssubnetid2 = None

    def get_username(self):
        return self.username

    def get_awssecret(self):
        return self.awssecret

    def get_awstoken(self):
        return self.awstoken

    def get_awsregion(self):
        return self.awsregion

    def get_awspubkeyname(self):
        return self.awspubkeyname

    def get_awssubnetid2(self):
        return self.awssubnetid2

    def set_username(self, username):
        self.username = username

    def set_awssecret(self, awssecret):
        self.awssecret = awssecret

    def set_awstoken(self, awstoken):
        self.awstoken = awstoken

    def set_awsregion(self, awsregion):
        self.awsregion = awsregion

    def set_awspubkeyname(self, awspubkeyname):
        self.awspubkeyname = awspubkeyname

    def set_awssubnetid2(self, awssubnetid2):
        self.awssubnetid2 = awssubnetid2
