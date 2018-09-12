#!/usr/bin/env python

import sys
from scalectldaemon import ScaleCtlDaemon
from scalectlclient import ScaleCtlClient


if __name__ == "__main__":
    # Setup variables
    alias = 'scalectl'
    api = 'api/v1/'
    host = 'localhost'
    port = 8081

    # Setup scalectl client
    scalectlclient = ScaleCtlClient(alias, port, api)
    scalectlclient.setup_hostfile()

    # Setup scalectl daemon (if not already running)
    scalectldaemon = ScaleCtlDaemon('/tmp/scalectl-daemon.pid', 'ScaleAPI', host, port)

    # Argument handling (client)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            scalectldaemon.start()
        elif 'stop' == sys.argv[1]:
            scalectldaemon.stop()
        elif 'restart' == sys.argv[1]:
            scalectldaemon.restart()
        elif 'setup' == sys.argv[1]:
            print '"%s %s" requires exactly 1 argument\n' % (sys.argv[0], sys.argv[1])
            print 'Usage: %s %s USERNAME\n' % (sys.argv[0], sys.argv[1])
            print 'Fetch the AWS data from the ScaleX database for USERNAME\n'
            print 'Options:'
            print '  --force      Reinitialize scalectl with provided user'
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
                print '  --size             Set the initial size of the cluster'
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
                sys.exit(2)
        elif 'setup' == sys.argv[1]:
            response = scalectlclient.get_active_user()
            if response == "False":
                print 'No active user detected! Setting up %s' % sys.argv[2]
                response = scalectlclient.setup_user(sys.argv[2])
                print response
            else:
                print 'scalectl already setup for user %s\n' % response
                print 'Use --force to overwrite!'
                sys.exit(2)
        sys.exit(0)
    elif len(sys.argv) == 4:
        if 'setup' == sys.argv[1] and '--force' == sys.argv[2]:
            print 'Setting up %s' % sys.argv[3]
            response = scalectlclient.setup_user(sys.argv[3])
            print response
        elif 'cluster' == sys.argv[1] and 'status' == sys.argv[2]:
            if '--all' == sys.argv[3]:
                response = scalectlclient.cluster_status()
                print response
            else:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Retrieve the status and metrics of a or all running cluster/s\n'
                print 'Options:'
                print '  --all      Displays all running clusters and their metrics'
        sys.exit(0)
    else:
        print 'Usage: %s COMMAND\n' % sys.argv[0]
        print 'Commands: '
        print '  start		Starts the scalectl-daemon'
        print '  stop		Stops the scalectl-daemon'
        print '  restart	Restarts the scalectl-daemon'
        print '  setup		Fetches AWS information from the ScaleX database'
        print '  cluster	Controls and Creates AWS autoscaling clusters'
        sys.exit(2)
