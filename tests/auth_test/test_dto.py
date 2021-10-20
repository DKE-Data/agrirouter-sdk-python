"""Tests agrirouter/auth/dto.py"""
from agrirouter.onboarding.dto import (
    AuthorizationToken,
    ConnectionCriteria,
    Authentication,
)
from agrirouter.messaging.exceptions import WrongFieldError
import pytest


class TestAuthorizationToken:
    def test_json_deserialize(self):
        account = "account"
        regcode = "regcode"
        expires = "01-01-2021"
        test_object = AuthorizationToken(
            account=account,
        )
        test_object.json_deserialize({"regcode": regcode, "expires": expires})
        assert test_object
        assert test_object.account == account
        assert test_object.regcode == regcode
        assert test_object.expires == expires

        test_object_1 = AuthorizationToken(
            regcode=regcode,
        )
        test_object_1.json_deserialize({"account": account})
        assert test_object_1
        assert test_object_1.account == account
        assert test_object_1.regcode == regcode
        assert test_object_1.expires is None

        test_object_2 = AuthorizationToken(
            account=account,
        )
        test_object_2.json_deserialize({"expires": expires})
        assert test_object_2
        assert test_object_2.account == account
        assert test_object_2.regcode is None
        assert test_object_2.expires == expires

        test_object_3 = AuthorizationToken(
            expires=expires,
        )
        test_object_3.json_deserialize({"regcode": regcode})
        assert test_object_3
        assert test_object_3.account is None
        assert test_object_3.regcode == regcode
        assert test_object_3.expires == expires
        with pytest.raises(WrongFieldError):
            assert test_object_3.json_deserialize({"wrong_key": regcode})


class TestConnectionCriteria:
    def test_json_deserialize(self):
        client_id = "1"
        commands = "commands"
        gateway_id = "3"
        host = "localhost"
        measures = "test_measures"
        port = "80"
        test_object = ConnectionCriteria(
            gateway_id=gateway_id,
            client_id=client_id,
            host=host,
            measures=measures,
            port=port,
        )
        test_object.json_deserialize({"commands": commands})
        assert test_object
        assert test_object.gateway_id == gateway_id
        assert test_object.client_id == client_id
        assert test_object.commands == commands
        assert test_object.host == host
        assert test_object.measures == measures
        assert test_object.port == port

        test_object_1 = ConnectionCriteria(
            gateway_id=gateway_id,
            client_id=client_id,
            commands=commands,
            measures=measures,
            port=port,
        )

        test_object_1.json_deserialize({"host": host})
        assert test_object_1
        assert test_object_1.gateway_id == gateway_id
        assert test_object_1.client_id == client_id
        assert test_object_1.commands == commands
        assert test_object_1.host == host
        assert test_object_1.measures == measures
        assert test_object_1.port == port
        with pytest.raises(WrongFieldError):
            assert test_object_1.json_deserialize({"wrong_key": measures})


class TestAuthentication:
    def test_json_deserialize(self):
        type = "type"
        secret = "secret"
        certificate = "certificate"
        test_object = Authentication(
            type=type,
            secret=secret,
        )
        test_object.json_deserialize({"certificate": certificate})
        assert test_object
        assert test_object.type == type
        assert test_object.secret == secret
        assert test_object.certificate == certificate

        test_object_1 = Authentication(type=type, certificate=certificate)
        test_object_1.json_deserialize({"secret": secret})
        assert test_object_1
        assert test_object_1.type == type
        assert test_object_1.secret == secret
        assert test_object_1.certificate == certificate

        test_object_2 = Authentication(secret=secret, certificate=certificate)
        test_object_2.json_deserialize({"type": type})
        assert test_object_2
        assert test_object_2.type == type
        assert test_object_2.secret == secret
        assert test_object_2.certificate == certificate

        test_object_2 = Authentication(
            secret=secret,
        )
        test_object_2.json_deserialize({"type": type})
        assert test_object_2
        assert test_object_2.type == type
        assert test_object_2.secret == secret
        assert test_object_2.certificate is None
        with pytest.raises(WrongFieldError):
            assert test_object_2.json_deserialize({"wrong_key": certificate})
