

class InvalidEnvironmentSetup(Exception):

    def __init__(self, message=None, env=None):
        if not message:
            message = "Invalid value of env parameter. [QA] or [Production] values are allowed"
        self.message = message
        self.env = env


class BadAuthResponse(Exception):
    def __init__(self, message=None):
        if not message:
            message = "Bad Response. Response could is not verified."
        self.message = message
