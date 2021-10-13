from agrirouter.environments.exceptions import InvalidEnvironmentSetup
from agrirouter.environments.environments import ProductionEnvironment, QAEnvironment


class EnvironmentalService:
    def __init__(self, env):
        self._set_env(env)

    def _set_env(self, env) -> None:
        if env == "QA":
            self._environment = QAEnvironment()
        elif env == "Production":
            self._environment = ProductionEnvironment()
        else:
            raise InvalidEnvironmentSetup(env=env)
