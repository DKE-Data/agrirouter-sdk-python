from agrirouter.environments.environments import ProductionEnvironment, QAEnvironment
from agrirouter.environments.exceptions import InvalidEnvironmentSetup


class EnvironmentalService:
    def __init__(self, env):
        if type(env) is str:
            self._set_env(env)
        else:
            self._environment = env

    def _set_env(self, env) -> None:
        if env == "QA":
            self._environment = QAEnvironment()
        elif env == "Production":
            self._environment = ProductionEnvironment()
        else:
            raise InvalidEnvironmentSetup(env=env)
