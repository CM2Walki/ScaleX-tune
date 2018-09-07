#!/usr/bin/env python

import requests, sys


class TunexClient:
    def __init__(self, alias, port, api):
        self.alias = alias
        self.port = port
        self.api = api
        self.url = 'http://%s:%s/%s' % (alias, port, api)

    @staticmethod
    def setup_hostfile():
        with open("/etc/hosts", "r+") as f:
            for line in f:
                if '127.0.0.1	tunex' in line:
                    break
            else:
                file.write('127.0.0.1	tunex')

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
        print response.url
        if response.status_code == 200:
            return response.text
        else:
            print 'Daemon encountered an error (Code: %s)' % response.status_code
            sys.exit(2)
