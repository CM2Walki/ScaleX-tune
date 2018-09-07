#!/usr/bin/env python


import time
import gevent.monkey
from gevent.pywsgi import WSGIServer
from daemon import Daemon
from mongodb import MongoDatabase
from storage import Storage
from commands import Commands
from flask import Flask, Response
from flask_classy import FlaskView, route

gevent.monkey.patch_all()


class APIView(FlaskView):
    route_prefix = '/v1/'

    @route('/')
    def index(self):
        return "Test just a test\n"


class TunexDaemon(Daemon):
    app = None

    def __init__(self, pidfile, name, host, port):
        Daemon.__init__(self, pidfile)
        self.mongodbORM = None
        self.userStorage = None
        self.commandList = None
        self.host = host
        self.port = port
        self.app = Flask(name)
        APIView.register(self.app)

    def run(self):
        self.mongodbORM = MongoDatabase('localhost', 27017)
        self.userStorage = Storage()
        self.commandList = Commands(self.mongodbORM, self.userStorage)
        http_server = WSGIServer((self.host, self.port), self.app)
        http_server.serve_forever()
        while True:
            time.sleep(1)
