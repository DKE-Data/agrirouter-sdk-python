from uuid import uuid4

from agrirouter.api.enums import ResponseTypes


class AuthUrlParameter:
    def __init__(
            self, application_id: str,
            response_type: str,
            state: str = None,
            redirect_uri: str = ""
    ):

        self.application_id = application_id
        self.validate_response_type(response_type)
        self.response_type = response_type
        if not state:
            state = self.generate_unique_state()
        self.state = state
        self.redirect_uri = redirect_uri

    def get_parameters(self) -> dict:
        return {
            "application_id": self.application_id,
            "response_type": self.response_type,
            "state": self.state,
            "redirect_uri": self.redirect_uri,
        }

    def _state_is_none(self) -> bool:
        return not bool(self.state)

    def set_state(self) -> None:
        self.state = self.generate_unique_state()

    @staticmethod
    def generate_unique_state() -> str:
        return str(uuid4())

    @staticmethod
    def validate_response_type(response_type) -> None:
        if response_type not in ResponseTypes.values_list():
            raise ValueError("Invalid response_type parameter value.")
