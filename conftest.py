import pytest
from tests.constants import public_key, private_key, auth_result_url


@pytest.fixture(scope="session")
def authorization():
    from agrirouter.auth.auth import Authorization

    auth_client = Authorization("QA", public_key=public_key, private_key=private_key)
    auth_response = auth_client.extract_auth_response(auth_result_url)
    auth_client.verify_auth_response(auth_response)
    auth_data = auth_response.get_auth_result()
    return auth_data
