from agrirouter.auth.enums import Environments
from agrirouter.environments.environments import Production, QA
from agrirouter.environments.exceptions import InvalidEnvironmentSetup


class EnvironmentalService:
    """
    A class that provides environmental services based on the provided environment value.

    Attributes:
    - _environment (Environment): The current environment.
    """

    def __init__(self, env: str):
        self._set_env(env)

    def _set_env(self, env) -> None:
        """
        Sets the environment based on the provided value.

        Parameters:
        - env (str): The desired environment value. Must be one of the following: `qa` or `production`.

        Raises:
        - InvalidEnvironmentSetup: If the provided environment value is not valid.
        """
        if env == Environments.QA.value:
            self._environment = QA()
        elif env == Environments.PRODUCTION.value:
            self._environment = Production()
        else:
            raise InvalidEnvironmentSetup(env=env)
