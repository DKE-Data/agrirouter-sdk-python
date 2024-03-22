import json
import os

import tests
from src.onboarding.response import OnboardResponse


def read_onboard_response(identifier: str) -> OnboardResponse:
    """
    Read a recorded onboard response from the filesystem.
    """
    path = _get_path_for_onboard_responses(identifier)
    with open(path) as f:
        contents = f.read()
    onboard_response = OnboardResponse()
    onboard_response.json_deserialize(contents)
    return onboard_response


def save_onboard_response(identifier: str, onboard_response: OnboardResponse):
    """
    Save a recorded onboard response to the filesystem.
    """
    path = _get_path_for_onboard_responses(identifier)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = json.dumps(onboard_response.json_serialize())
    with open(path, 'w') as f:
        f.write(data)


def _get_path_for_onboard_responses(identifier: str) -> str:
    """
    Get the path to a recorded onboard response.
    """
    path = os.path.join(
        os.path.dirname(tests.__file__),
        f"data/onboarding_responses/{identifier}.json"
    )
    return path
