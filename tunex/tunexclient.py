#!/usr/bin/env python

import requests


class TunexClient:
    def __init__(self, p_alias, p_port, p_api):
        self.alias = p_alias
        self.port = p_port
        self.api = p_api
        self.url = 'http://%s:%s/%s' % (p_alias, p_port, p_api)

    def setup_hostfile(self):
        with open("/etc/hosts", "r+") as f:
            for line in f:
                if '127.0.0.1	tunex' in line:
                    break
            else:
                file.write('127.0.0.1	tunex')

    def get_active_user(self):
        return requests.get('%s%s' % (self.url, 'get_active_user'))