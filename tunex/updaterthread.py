#!/usr/bin/env python

import threading
import time
import datetime
import socket
import requests


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
        probes = 0
        total_lat = 0.0
        total_resp = 0.0
        while True:
            if not self.stop:
                now = datetime.datetime.now()
                if now.second > 0:
                    if counter > 10:
                        # Latency
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        start = time.time()
                        s.connect((str(self.target), 80))
                        total_lat = total_lat + (1000 * (time.time()-start))
                        s.close()
                        # Response Time
                        start = time.time()
                        # Make sure to process the headers and the data!
                        r = requests.get((str(self.target)), stream=True)
                        for chunk in r.iter_content(chunk_size=1024):
                            print ""
                        total_resp = total_resp + (1000 * (time.time() - start))
                        counter = 1
                        probes = probes + 1
                    counter = counter + 1
                else:
                    if probes > 0:
                        total_lat = total_lat / probes
                        total_resp = total_resp / probes
                    else:
                        # Latency
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        start = time.time()
                        s.connect((str(self.target), 80))
                        total_lat = (1000 * (time.time() - start))
                        s.close()
                        # Response Time
                        start = time.time()
                        # Make sure to process the headers and the data!
                        r = requests.get((str(self.target)), stream=True)
                        for chunk in r.iter_content(chunk_size=1024):
                            print ""
                        total_resp = (1000 * (time.time() - start))
                    self.mongodb.add_datapoint(self.username, total_lat, total_resp, int(time.time()))
                    probes = 0
                    total_lat = 0.0
                    total_resp = 0.0
                    counter = 1
                time.sleep(self.interval)
            else:
                break
        return

    # db.inventory.insert({"username": "Walki", "LatencyDatapoints": [], "ResponseTimeDatapoints": []})
    # db.inventory.findOne({username: "Walki"})
    # db.inventory.update({ username: "Walki" },{$push: {LatencyDatapoints: {$each: [ { "Timestamp": "test2", "Average": 8 } ],$sort: { "Timestamp": -1 },$slice: 60}}})
