#!/usr/bin/env python

import sys
from scalectldaemon import ScaleCtlDaemon
from scalectlclient import ScaleCtlClient


if __name__ == "__main__":
    # Setup variables
    alias = 'scalectl'
    api = 'api/v1/'
    host = 'localhost'
    port = 8085

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
            print '  --force\t\tReinitialize scalectl with provided user'
        elif 'cluster' == sys.argv[1]:
            print 'Usage: %s %s COMMAND\n' % (sys.argv[0], sys.argv[1])
            print 'Commands: '
            print '  run\t\tCreates a new AWS autoscaling group that runs the provided k8s deployment'
            print '  remove\tRemoves an AWS autoscaling group'
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    elif len(sys.argv) == 3:
        if 'cluster' == sys.argv[1]:
            if 'run' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [DEPLOYMENT]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Creates a new autoscaling cluster with the provided parameters on AWS\n'
                print 'Options:'
                print '  --name\t\t\tSet a name for the new cluster'
                print '  --size\t\t\tSet the initial size of the cluster'
                print '  --target\t\t\tSet the target domain of the cluster'
                print '  --function\t\t\tSet the load function (Example: x^2)'
            elif 'remove' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER] \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Removes a given cluster or removes all of them\n'
                print 'Options:'
                print '  --all\t\t\tRemove all clusters'
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
        sys.exit(0)
    else:
        print 'Usage: %s COMMAND\n' % sys.argv[0]
        print 'Commands: '
        print '  start\t\t\tStarts the scalectl-daemon'
        print '  stop\t\t\tStops the scalectl-daemon'
        print '  restart\t\tRestarts the scalectl-daemon'
        print '  setup\t\t\tFetches AWS information from the ScaleX database'
        print '  cluster\t\tControls and Creates AWS autoscaling clusters'
        sys.exit(2)
