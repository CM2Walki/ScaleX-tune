#!/usr/bin/env python


import requests, sys


class TunexClient:
    def __init__(self, alias, port, api):
        self.alias = alias
        self.port = port
        self.api = api
        self.url = 'http://%s:%s/%s' % (alias, port, api)

    def setup_hostfile(self):
        with open("/etc/hosts", "r+") as f:
            for line in f:
                if '127.0.0.1	%s' % self.alias in line:
                    break
            else:
                f.write('127.0.0.1	%s' % self.alias)

    def build_request(self, query):
        return '%s%s' % (self.url, query)

    def get_active_user(self):
        response = requests.get(self.build_request('get_active_user'))
        if response.status_code == 200:
            return response.text
        else:
            print 'Daemon encountered an error (Code: %s)' % response.status_code
            sys.exit(2)

    def setup_user(self, username):
        response = requests.get(self.build_request('setup_user'), params={'username': str(username)})
        if response.status_code == 200:
            return response.text
        else:
            print 'Daemon encountered an error (Code: %s)' % response.status_code
            sys.exit(2)
