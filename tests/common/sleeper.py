import time


class Sleeper:
    """ Sleep for a given amount of time. """

    @staticmethod
    def process_the_command(seconds: int = 15):
        """ Let the src process the command. To ensure clean message handling,
        we need to set the sleep time to 15 seconds. """
        time.sleep(seconds)

    @staticmethod
    def process_the_message(seconds: int = 30):
        """ Let the src process and route the message. To ensure clean message handling,
        we need to set the sleep time to 30 seconds. """
        time.sleep(seconds)
