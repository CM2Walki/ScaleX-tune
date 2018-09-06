#!/usr/bin/env python

import sys, os, time, threading
from daemon import Daemon
from mongodb import MongoDatabase
from storage import Storage
from commands import Commands
from socket import *


class TunexDaemon(Daemon):
    def __init__(self, pidfile, socket_path):
        Daemon.__init__(self, pidfile)
        self.mongodbORM = MongoDatabase('localhost', 27017)
        self.userStorage = Storage()
        self.commandList = Commands(self.mongodbORM, self.userStorage)
        self.socket_path = socket_path

    def handle_client(self, conn):
        with conn.makefile() as f:
            if f[0] == 'userStorage.get_username()':
                result = self.userStorage.get_username()
                conn.send(result)
            conn.close()

    def run(self):
        try:
            os.unlink(self.socket_path)
        except OSError:
            if os.path.exists(self.socket_path):
                raise
        server = socket(AF_UNIX, SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen(1)
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=[conn])
            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    socket_path = '/var/run/tunex.sock'
    daemon = TunexDaemon('/tmp/tunex-daemon.pid', socket_path)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'setup' == sys.argv[1]:
            print '"%s %s" requires exactly 1 argument\n' % (sys.argv[0], sys.argv[1])
            print 'Usage: %s %s [USERNAME]\n' % (sys.argv[0], sys.argv[1])
            print 'Fetch the AWS data from the ScaleX database for [USERNAME]\n'
            print 'Options:'
            print '  --force      Reinitialize tunex with provided user'
        elif 'cluster' == sys.argv[1]:
            print 'Usage: %s %s COMMAND\n' % (sys.argv[0], sys.argv[1])
            print 'Commands: '
            print '  status     Prints status information and metrics for cluster'
            print '  run        Creates a new AWS autoscaling group that runs the provided k8s deployment'
            print '  remove     Removes an AWS autoscaling group'
            print '  apply      Creates or replaces the deployment on a cluster'
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    elif len(sys.argv) == 3:
        client = socket(AF_UNIX, SOCK_STREAM)
        client.connect(socket_path)
        if 'cluster' == sys.argv[1]:
            if 'status' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Retrieve the status and metrics of a or all running cluster/s\n'
                print 'Options:'
                print '  --all      Displays all running clusters and their metrics'
            elif 'run' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [DEPLOYMENT]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Creates a new autoscaling cluster with the provided parameters on AWS\n'
                print 'Options:'
                print '  --name             Set a name for the new cluster'
                print '  --cpuscaleutil     Set the average cpu utilization scaling threshold'
                print '  --loadbalancer     Create a loadbalancer attached to the scaling group'
            elif 'remove' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER] \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Removes a given cluster or removes all of them\n'
                print 'Options:'
                print '  --all      Remove all clusters'
            elif 'apply' == sys.argv[2]:
                print '"%s %s %s" requires at least 2 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s CLUSTER DEPLOYMENT \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Creates or replaces the deployment on a cluster\n'
            else:
                print "Unknown command"
                client.close()
                sys.exit(2)
        elif 'setup' == sys.argv[1]:
            client.send('userStorage.get_username()')
            data = client.recv(1024)
            client.close()
            if data is None:
                print 'Do things' #TunexDaemon.commandList.setupUser(sys.argv[2])
            else:
                print 'tunex already setup for user %s\n'# + TunexDaemon.userStorage.get_username()
                print 'Use --force to overwrite!'
                client.close()
                sys.exit(2)
        client.close()
        sys.exit(0)
    elif len(sys.argv) == 5:
        client = socket(AF_UNIX, SOCK_STREAM)
        client.connect(socket_path)
        if 'setup' == sys.argv[2] and '--force' == sys.argv[3]:
            print 'Do Things' #TunexDaemon.commandList.setupUser(sys.argv[4])
        client.close()
        sys.exit(0)
    else:
        print 'Usage: %s COMMAND\n' % sys.argv[0]
        print 'Commands: '
        print '  start		Starts the tunex-daemon'
        print '  stop		Stops the tunex-daemon'
        print '  restart	Restarts the tunex-daemon'
        print '  setup		Fetches AWS information from the ScaleX database'
        print '  cluster	Controls and Creates AWS autoscaling clusters'
        sys.exit(2)
