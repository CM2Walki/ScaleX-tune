#!/usr/bin/env python


import time
import gevent.monkey
from gevent.pywsgi import WSGIServer
from daemon import Daemon
from mongodb import MongoDatabase
from storage import Storage
from daemoncommands import DaemonCommands
from flask import Flask, Response
from flask_classy import FlaskView, route


gevent.monkey.patch_all()


class V1View(FlaskView):
    route_prefix = '/api/'

    def __init__(self):
        FlaskView.__init__(self)
        self.mongodbORM = MongoDatabase('localhost', 27017)
        self.userStorage = Storage()
        self.commandList = DaemonCommands(self.mongodbORM, self.userStorage)

    @route('/')
    def index(self):
        return ""

    @route('/get_active_user')
    def get_username(self):
        return self.commandList.get_active_user()

    @route('/setup_user/<username>')
    def setup_user(self, username):
        return self.commandList.setup_user(str(username))


class TunexDaemon(Daemon):
    app = None

    def __init__(self, pidfile, name, host, port):
        Daemon.__init__(self, pidfile)
        self.app = None
        self.host = host
        self.port = port
        self.name = name

    def run(self):
        self.app = Flask(self.name)
        V1View.register(self.app)
        http_server = WSGIServer((self.host, self.port), self.app)
        http_server.serve_forever()
