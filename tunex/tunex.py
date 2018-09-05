#!/usr/bin/env python

import sys, time, boto3
from daemon import Daemon
from pymongo import MongoClient


class TunexDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)


class MongoDatabase():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)


if __name__ == "__main__":
    daemon = TunexDaemon('/tmp/tunex-daemon.pid')
    mongodb = MongoDatabase()
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
            print 'Fetch the AWS data from the ScaleX database for [USERNAME]'
        elif 'cluster' == sys.argv[1]:
            print 'Usage: %s %s COMMAND\n' % (sys.argv[0], sys.argv[1])
            print 'Commands: '
            print '  status		Prints status information and metrics for cluster'
            print '  run        Creates a new AWS autoscaling group that runs the provided k8s deployment'
            print '  remove		Removes an AWS autoscaling group'
            print '  apply		Creates or replaces the deployment on a cluster'
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    if len(sys.argv) == 3:
        if 'cluster' == sys.argv[1]:
            if 'status' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Retrieve the status and metrics of a or all running cluster/s\n'
                print 'Options:'
                print '  --all      Displays all running clusters and their metrics'
            elif 'run' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
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
        print 'Usage: %s COMMAND\n' % sys.argv[0]
        print 'Commands: '
        print '  start		Starts the tunex-daemon'
        print '  stop		Stops the tunex-daemon'
        print '  restart	Restarts the tunex-daemon'
        print '  setup		Fetches AWS information from the ScaleX database'
        print '  cluster	Controls and Creates AWS autoscaling clusters'
        sys.exit(2)