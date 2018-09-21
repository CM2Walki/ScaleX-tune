#!/usr/bin/env python

import threading
import time
import datetime
import socket


class Updater(object):
    """ Threading class
    Taken from: http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
    """

    def __init__(self, interval, target, mongodb, username):
        self.interval = interval
        self.target = target
        self.mongodb = mongodb
        self.username = username
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()
        self.stop = False

    def delete(self):
        self.stop = True

    def run(self):
        self.mongodb.create_perf_data_db(self.username)
        counter = 1
        total = 0.0
        while True:
            if not self.stop:
                now = datetime.datetime.now()
                if now.second > (self.interval+1):
                    if counter > 5:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        start = time.time()
                        s.connect((str(self.target), 80))
                        runtime = (1000 * (time.time()-start))
                        total = total + runtime
                        s.close()
                    else:
                        counter = 1
                        total = 0.0
                    counter = counter + 1
                else:
                    total = total / counter
                    self.mongodb.add_latency_datapoint(self.username, total, int(time.time()))
                    total = 0.0
                    counter = 1
                time.sleep(self.interval)
            else:
                break
        return

    # db.inventory.insert({"username": "Walki", "LatencyDatapoints": [], "ResponseTimeDatapoints": []})
    # db.inventory.findOne({username: "Walki"})
    # db.inventory.update({ username: "Walki" },{$push: {LatencyDatapoints: {$each: [ { "Timestamp": "test2", "Average": 8 } ],$sort: { "Timestamp": -1 },$slice: 60}}})
