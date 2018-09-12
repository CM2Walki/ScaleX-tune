import threading
import time


class Updater(object):
    """ Threading class
    Taken from: http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
    """

    def __init__(self, interval, cluster_list, cluster_stats, auto_scaling, ec2, elb):
        self.interval = interval
        self.cluster_list = cluster_list
        self.cluster_stats = cluster_stats
        self.auto_scaling = auto_scaling
        self.ec2 = ec2
        self.elb = elb

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            time.sleep(self.interval)
