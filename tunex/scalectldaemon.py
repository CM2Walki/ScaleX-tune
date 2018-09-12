#!/usr/bin/env python


import gevent.monkey
from gevent.pywsgi import WSGIServer
from daemon import Daemon
from mongodb import MongoDatabase
from storage import Storage
from daemoncommands import DaemonCommands
from flask import Flask, request
from flask_classy import FlaskView, route


gevent.monkey.patch_all()

mongodbORM = MongoDatabase('localhost', 27017)
userStorage = Storage()
commandList = DaemonCommands(mongodbORM, userStorage)


class V1View(FlaskView):
    route_prefix = '/api/'

    @route('/')
    def index(self):
        return ""

    @route('/get_active_user')
    def get_username(self):
        return commandList.get_active_user()

    @route('/setup_user')
    def setup_user(self):
        username = str(request.args.get('username'))
        return commandList.setup_user(username)

    @route('/cluster_status')
    def cluster_status(self):
        return commandList.cluster_status()

    @route('/cluster_run')
    def cluster_run(self):
        return commandList.cluster_status()


class ScaleCtlDaemon(Daemon):
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
