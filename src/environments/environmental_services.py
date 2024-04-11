from src.api.environments import BaseEnvironment


class EnvironmentalService:
    """
    A class that provides environmental services based on the provided environment value.

    Attributes:
    - _environment (Environment): The current environment.
    """

    def __init__(self, env: BaseEnvironment):
        self._set_env(env)

    def _set_env(self, env) -> None:
        """
        Sets the environment based on the provided value.

        Parameters:
        - env (str): The desired environment value. Must be one of the following: `qa` or `production`.

        Raises:
        - InvalidEnvironmentSetup: If the provided environment value is not valid.
        """
        self._environment = env
