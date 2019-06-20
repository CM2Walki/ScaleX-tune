#!/usr/bin/env python

import sys, os
from scalexctldaemon import ScaleXCtlDaemon
from scalexctlclient import ScaleXCtlClient


if __name__ == "__main__":
    # Setup variables
    alias = 'scalexctl'
    api = 'api/v1/'
    host = os.environ['DAEMON_HOST']
    port = 20000

    # Setup scalexctl client
    scalexctlclient = ScaleXCtlClient(alias, port, api)
    scalexctlclient.setup_hostfile()

    # Setup scalexctl daemon (if not already running)
    scalexctldaemon = ScaleXCtlDaemon('/tmp/scalexctl-daemon.pid', 'ScaleXAPI', host, port)

    # Argument handling (client)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            scalexctldaemon.start()
        elif 'stop' == sys.argv[1]:
            scalexctldaemon.stop()
        elif 'restart' == sys.argv[1]:
            scalexctldaemon.restart()
        elif 'setup' == sys.argv[1]:
            print '"%s %s" requires exactly 1 argument\n' % (sys.argv[0], sys.argv[1])
            print 'Usage: %s %s USERNAME\n' % (sys.argv[0], sys.argv[1])
            print 'Fetch the AWS data from the ScaleX database for USERNAME\n'
            print 'Options:'
            print '  --force\t\tReinitialize scalexctl with provided user'
        elif 'cluster' == sys.argv[1]:
            print 'Usage: %s %s COMMAND\n' % (sys.argv[0], sys.argv[1])
            print 'Commands: '
            print '  run\t\tCreates a new AWS autoscaling group that runs a benchmark against the provided target'
            print '  remove\tRemoves an AWS autoscaling group'
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    elif len(sys.argv) == 3:
        if 'cluster' == sys.argv[1]:
            if 'run' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [ARGUMENTS] \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Example: %s %s %s 0 2147483647 60 "1.2.3.4" "(-1)*(x-10)^2+100" 8 t2.micro' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print '\t\t\t\t\t\tTIMESTART TIMEEND TIMESTEP TARGET FUNCTION CLUSTERSIZE INSTANCETYPE'
                print 'Creates a new autoscaling benchmark cluster with the provided parameters on AWS\n'
            elif 'remove' == sys.argv[2]:
                response = scalexctlclient.cluster_remove()
                print response
            else:
                print "Unknown command"
                sys.exit(2)
        elif 'setup' == sys.argv[1]:
            response = scalexctlclient.get_active_user()
            if response == "False":
                print 'No active user detected! Setting up %s' % sys.argv[2]
                response = scalexctlclient.setup_user(sys.argv[2])
                print response
            else:
                print 'scalexctl already setup for user %s\n' % response
                print 'Use --force to overwrite!'
                sys.exit(2)
        elif 'start' == sys.argv[1]:
            if '--attach' == sys.argv[2]:
                scalexctldaemon.start(True)
                sys.exit(0)
        sys.exit(0)
    elif len(sys.argv) == 4:
        if 'setup' == sys.argv[1] and '--force' == sys.argv[2]:
            print 'Setting up %s' % sys.argv[3]
            response = scalexctlclient.setup_user(sys.argv[3])
            print response
        sys.exit(0)
    elif len(sys.argv) > 4:
        if 'cluster' == sys.argv[1]:
            if 'run' == sys.argv[2]:
                print 'Setting up %s' % sys.argv[1]
                print 'Timestart = %s; Timeend = %s; Timestep = %s; Target = %s; Function = %s; Size = %s; Instancetype: %s\n' % (sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
                response = scalexctlclient.cluster_run(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
                print response
    else:
        print 'Usage: %s COMMAND\n' % sys.argv[0]
        print 'Commands: '
        print '  start\t\t\tStarts the scalexctl-daemon'
        print '  stop\t\t\tStops the scalexctl-daemon'
        print '  restart\t\tRestarts the scalexctl-daemon'
        print '  setup\t\t\tFetches AWS information from the ScaleX database'
        print '  cluster\t\tControls and Creates AWS autoscaling clusters'
        sys.exit(2)
