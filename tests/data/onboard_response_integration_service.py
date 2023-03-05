from agrirouter.onboarding.response import OnboardResponse
import sys, os
import tests
import json

class OnboardResponseIntegrationService:
    @staticmethod
    def read(identifier: str) -> OnboardResponse:
        path = OnboardResponseIntegrationService._get_path(identifier)
        with open(path) as f:
            contents = f.read()
        onboard_response = OnboardResponse()
        onboard_response.json_deserialize(contents)
        return onboard_response

    @staticmethod
    def save(identifier: str, onboard_response: OnboardResponse):
        path = OnboardResponseIntegrationService._get_path(identifier)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = json.dumps(onboard_response.json_serialize())
        with open(path, 'w') as f:
            f.write(data)

    @staticmethod
    def _get_path(identifier: str) -> str:
        path = os.path.join(
            os.path.dirname(tests.__file__),
            f"data/onboarding_responses/{identifier}.json"
        )
        return path
