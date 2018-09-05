#!/usr/bin/env python

import sys, time
from daemon import Daemon
from pymongo import MongoClient

class TuneDaemon(Daemon):
	def run(self):
		while True:
			time.sleep(1)

class MongoDatabase():
	def __init__(self):
		self.client = MongoClient('localhost', 27017)

if __name__ == "__main__":
	daemon = TuneDaemon('/tmp/tune-daemon.pid')
	mongodb = MongoDatabase()
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'setup' == sys.argv[1]:
			print '"%s setup" requires exactly 1 argument\n'
			print 'Usage: %s setup [username]'
		elif 'cluster' == sys.argv[1]:
			print 'Usage: %s cluster status|run|remove|change' % sys.argv[0]
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print 'Usage: %s COMMAND' % sys.argv[0]
		sys.exit(2)
