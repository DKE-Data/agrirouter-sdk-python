import time


class Sleeper:
    """ Sleep for a given amount of time. """

    @staticmethod
    def let_agrirouter_process_the_message(seconds: int = 30):
        """ Let the agrirouter process the message. To ensure clean message handling, we need to set the sleep time to 30 seconds. """
        time.sleep(seconds)
