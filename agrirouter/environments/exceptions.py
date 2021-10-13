

class InvalidEnvironmentSetup(Exception):

    def __init__(self, message=None, env=None):
        if not message:
            message = "Invalid value of env parameter. [QA] or [Production] values are allowed. " \
                      "Please use environments.enums.Enviroments enum for configure environment properly"

        self.message = message
        self.env = env
