#!/usr/bin/env python


class Storage():
    def __init__(self):
        self.username = "NaN"
        self.awssecret = ""
        self.awstoken = ""
        self.awsregion = ""
        self.awspubkeyname = ""

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
