#!/usr/bin/env python


import requests
import sys


class ScaleCtlClient:
    def __init__(self, alias, port, api):
        self.alias = alias
        self.port = port
        self.api = api
        self.url = 'http://%s:%s/%s' % (alias, port, api)

    def setup_hostfile(self):
        with open("/etc/hosts", "r+") as f:
            for line in f:
                if '127.0.0.1\tscalectl\n' in line:
                    break
            else:
                f.write('127.0.0.1\tscalectl\n')

    def build_request(self, query):
        return '%s%s' % (self.url, query)

    def get_active_user(self):
        try:
            response = requests.get(self.build_request('get_active_user'))
        except requests.exceptions.ConnectionError:
            print 'Unable to contact HTTP server! Is the Daemon running?'
            sys.exit(2)
        if response.status_code == 200:
            return response.text
        else:
            print 'Daemon encountered an error (Code: %s)' % response.status_code
            sys.exit(2)

    def cluster_run(self, timestart, timeend, timestep, target, function, clustersize, instancetype):
        try:
            response = requests.get(self.build_request('cluster_run'), params={'timestart': str(timestart), 'timeend': str(timeend), 'timestep': str(timestep), 'target': str(target), 'function': str(function), 'clustersize': str(clustersize), 'instancetype': str(instancetype)})
        except requests.exceptions.ConnectionError:
            print 'Unable to contact HTTP server! Is the Daemon running?'
            sys.exit(2)
        if response.status_code == 200:
            return response.text
        else:
            print 'Daemon encountered an error (Code: %s)' % response.status_code
            sys.exit(2)

    def setup_user(self, username):
        try:
            response = requests.get(self.build_request('setup_user'), params={'username': str(username)})
        except requests.exceptions.ConnectionError:
            print 'Unable to contact HTTP server! Is the Daemon running?'
            sys.exit(2)
        if response.status_code == 200:
            return response.text
        else:
            print 'Daemon encountered an error (Code: %s)' % response.status_code
            sys.exit(2)
