import unittest

from agrirouter.api.enums import ResponseTypes
from agrirouter.api.environments import BaseEnvironment
from agrirouter.auth.auth import Authorization
from agrirouter.auth.parameters import AuthUrlParameter


class MockEnvironment(BaseEnvironment):
    def get_secured_onboarding_authorization_url(self, **kwargs):
        return 'https://secured.url'

    def get_env_public_key(self):
        return 'public_key_env'


class TestAuthorization(unittest.TestCase):

    def test_authorization_initialization(self):
        authorization = Authorization(MockEnvironment(), 'public_key', 'private_key')
        assert authorization._public_key == 'public_key'
        assert authorization._private_key == 'private_key'

    def test_get_auth_request_url(self):
        authorization = Authorization(MockEnvironment(), 'public_key', 'private_key')
        parameters = AuthUrlParameter(application_id='app_id', response_type=ResponseTypes.ONBOARD.value,
                                      state='state',
                                      redirect_uri='redirect_uri')
        auth_url = authorization.get_auth_request_url(parameters=parameters)
        assert auth_url == 'https://secured.url'

    def test_extract_auth_response(self):
        authorization = Authorization(MockEnvironment(), 'public_key', 'private_key')
        auth_response = authorization.extract_auth_response(
            'https://example.com/?state=state&token=token&signature=signature')
        assert auth_response.state == 'state'
        assert auth_response.token == 'token'
        assert auth_response.signature == 'signature'
        assert auth_response.error is None

    def test_extract_auth_response_and_error(self):
        authorization = Authorization(MockEnvironment(), 'public_key', 'private_key')
        auth_response = authorization.extract_auth_response(
            'https://example.com/?state=state&token=token&signature=signature&error=error')
        assert auth_response.state == 'state'
        assert auth_response.token == 'token'
        assert auth_response.signature == 'signature'
        assert auth_response.error == 'error'

    def test_extract_query_params(self):
        query_str = "param1=value1&param2=value2&param3=value3"
        extracted_params = Authorization._extract_query_params(query_str)
        expected_params = {'param1': 'value1', 'param2': 'value2', 'param3': 'value3'}
        assert extracted_params == expected_params
