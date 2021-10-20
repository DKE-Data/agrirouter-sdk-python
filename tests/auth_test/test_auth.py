"""Tests agrirouter/auth/auth.py"""

from agrirouter import AuthUrlParameter
from agrirouter.auth.auth import Authorization
from tests.constants import (
    public_key,
    private_key,
    auth_result_url,
    ENV,
    application_id,
)
from re import search


class TestAuthorization:
    def test_extract_auth_response(self):
        auth_client = Authorization(ENV, public_key=public_key, private_key=private_key)
        assert isinstance(auth_client.extract_auth_response(auth_result_url), object)
        assert search(
            "<agrirouter.auth.response.AuthResponse",
            str(auth_client.extract_auth_response(auth_result_url)),
        )

        auth_client = Authorization(
            "Production", public_key=public_key, private_key=private_key
        )
        assert search(
            "<agrirouter.auth.response.AuthResponse",
            str(auth_client.extract_auth_response(auth_result_url)),
        )

    def test_get_auth_request_url(self):
        auth_params = AuthUrlParameter(
            application_id=application_id, response_type="onboard"
        )
        auth_client = Authorization(
            "QA", public_key=public_key, private_key=private_key
        )
        check_url = "https://agrirouter-qa.cfapps.eu10.hana.ondemand.com/application/"
        assert search(check_url, auth_client.get_auth_request_url(auth_params))

    def test_get_auth_result(self):
        auth_client = Authorization(
            "QA", public_key=public_key, private_key=private_key
        )
        auth_response = auth_client.extract_auth_response(auth_result_url)
        auth_client.verify_auth_response(auth_response)
        assert auth_response.get_auth_result()["credentials"]
