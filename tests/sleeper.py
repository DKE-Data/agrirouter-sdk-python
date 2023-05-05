import time


class Sleeper:
    """ Sleep for a given amount of time. """

    @staticmethod
    def let_agrirouter_process_the_message(seconds: int = 8):
        """ Let the agrirouter process the message. """
        time.sleep(seconds)
