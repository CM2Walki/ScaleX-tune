import threading
import time


class Updater(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    Taken from: http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
    """

    def __init__(self, interval, cluster_list, cluster_stats):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.cluster_list = cluster_list
        self.cluster_stats = cluster_stats

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            self.cluster_stats.append("FREEDOM!")

            time.sleep(self.interval)
