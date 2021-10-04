from agrirouter.environments.environments import ProductionEnvironment, QAEnvironment


class InvalidEnvironmentSetup(Exception):
    def __init__(self, message=None, env=None):
        if not message:
            message = "Invalid value of env parameter. [QA] or [Production] values are allowed"
        self.message = message
        self.env = env


class ARClient:

    def __init__(self, env):
        self._set_env(env)

    def authenticate(self):
        auth_link = self._create_auth_link()

    def _create_auth_link(self):
        return ""

    def _set_env(self, env):
        if env == "QA":
            self._environment = QAEnvironment
        if env == "Production":
            return ProductionEnvironment
        else:
            raise InvalidEnvironmentSetup(env=env)
