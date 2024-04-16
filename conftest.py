import pytest

from agrirouter.api.enums import Environments
from tests.agrirouter.common.constants import PUBLIC_KEY, PRIVATE_KEY, AUTH_RESULT_URL


@pytest.fixture(scope="session")
def authorization():
    from agrirouter.auth.auth import Authorization

    auth_client = Authorization(Environments.QA.value, public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
    auth_response = auth_client.extract_auth_response(AUTH_RESULT_URL)
    auth_client.verify_auth_response(auth_response)
    auth_data = auth_response.get_auth_result()
    return auth_data
