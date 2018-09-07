#!/usr/bin/env python

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
from daemon import Daemon
from mongodb import MongoDatabase
from storage import Storage
from commands import Commands
from flask import Flask, Response


gevent.monkey.patch_all()


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

    def run(self):
        self.mongodbORM = MongoDatabase('localhost', 27017)
        self.userStorage = Storage()
        self.commandList = Commands(self.mongodbORM, self.userStorage)
        http_server = WSGIServer((self.host, self.port), self.app)
        http_server.serve_forever()

    @app.route('/')
    def users(self):
        return "Test"
