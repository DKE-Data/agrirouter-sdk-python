"""Tests agrirouter/onboarding/dto.py"""
from agrirouter.onboarding.dto import ConnectionCriteria, Authentication, ErrorResponse
from agrirouter.messaging.exceptions import WrongFieldError
import pytest


class TestConnectionCriteria:

    def test_json_deserialize_from_valid_dict(self):
        client_id = "1"
        commands = "commands"
        gateway_id = "3"
        host = "localhost"
        measures = "test_measures"
        port = "80"

        test_object = ConnectionCriteria()

        data = {"clientId": "1", "commands": "commands", "gatewayId": "3", "host": "localhost", "port": "80",
                "measures": "test_measures"}

        test_object.json_deserialize(data)
        assert test_object
        assert test_object.gateway_id == gateway_id
        assert test_object.client_id == client_id
        assert test_object.commands == commands
        assert test_object.host == host
        assert test_object.measures == measures
        assert test_object.port == port

    def test_json_deserialize_from_invalid_dict(self):
        test_object = ConnectionCriteria()

        with pytest.raises(WrongFieldError):
            test_object.json_deserialize({"clientId": "1", "commands": "commands", "wrong_key": "localhost"})

    def test_json_deserialize_from_valid_json(self):
        client_id = "1"
        commands = "commands"
        gateway_id = "3"
        host = "localhost"
        measures = "test_measures"
        port = "80"

        json_data = '{"clientId": "1", "commands": "commands", "gatewayId": "3", "host": "localhost", "port": "80",' \
                    '"measures": "test_measures"}'

        test_object = ConnectionCriteria()
        test_object.json_deserialize(json_data)
        assert test_object
        assert test_object.gateway_id == gateway_id
        assert test_object.client_id == client_id
        assert test_object.commands == commands
        assert test_object.host == host
        assert test_object.measures == measures
        assert test_object.port == port

    def test_json_deserialize_from_invalid_json(self):
        json_data = '{"client_id": "1", "commands": "commands", "wrong_key": "localhost"}'
        test_object = ConnectionCriteria()

        with pytest.raises(WrongFieldError):
            assert test_object.json_deserialize(json_data)

    def test_json_serialize(self):
        client_id = "1"
        commands = "commands"
        gateway_id = "3"
        host = "localhost"
        measures = "test_measures"
        port = "80"

        test_object = ConnectionCriteria(
            client_id=client_id,
            commands=commands,
            gateway_id=gateway_id,
            host=host,
            measures=measures,
            port=port
        )

        serialized_data = test_object.json_serialize()
        assert serialized_data["gatewayId"] == gateway_id
        assert serialized_data["clientId"] == client_id
        assert serialized_data["commands"] == commands
        assert serialized_data["host"] == host
        assert serialized_data["measures"] == measures
        assert serialized_data["port"] == port


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

    def test_json_deserialize_from_valid_dict(self):
        type = "type"
        secret = "secret"
        certificate = "certificate"

        test_object = Authentication()

        test_object.json_deserialize({"certificate": certificate, "type": type, "secret": secret})

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

    def test_json_deserialize_from_invalid_dict(self):
        test_object = Authentication()

        with pytest.raises(WrongFieldError):
            test_object.json_deserialize({"type": "type", "secret": "secret", "wrong_key": "certificate"})

    def test_json_deserialize_from_valid_json(self):
        type = "type"
        secret = "secret"
        certificate = "certificate"

        test_object = Authentication()
        json_data = '{"certificate": "certificate", "type": "type", "secret": "secret"}'

        test_object.json_deserialize(json_data)

        assert test_object
        assert test_object.type == type
        assert test_object.secret == secret
        assert test_object.certificate == certificate

    def test_json_deserialize_from_invalid_json(self):
        json_data = '{"type": "type", "secret": "secret", "wrong_key": "certificate"}'
        test_object = ConnectionCriteria()

        with pytest.raises(WrongFieldError):
            assert test_object.json_deserialize(json_data)

    def test_json_serialize(self):
        type = "type"
        secret = "secret"
        certificate = "certificate"

        test_object = Authentication(
            type=type,
            secret=secret,
            certificate=certificate
        )

        serialized_data = test_object.json_serialize()

        assert serialized_data
        assert serialized_data["type"] == type
        assert serialized_data["secret"] == secret
        assert serialized_data["certificate"] == certificate


class TestErrorResponse:

    def test_json_deserialize_from_valid_dict(self):
        code = "400"
        message = "message"
        target = "target"
        details = "details"

        data = {"code": code, "message": message, "target": target, "details": details}

        test_object = ErrorResponse()
        test_object.json_deserialize(data)
        assert test_object
        assert test_object.code == code
        assert test_object.message == message
        assert test_object.target == target
        assert test_object.details == details

    def test_json_deserialize_from_invalid_dict(self):
        data = {"code": "401", "message": "message", "wrong_field": "target"}
        test_object = ErrorResponse()

        with pytest.raises(WrongFieldError):
            assert test_object.json_deserialize(data)

    def test_json_deserialize_from_valid_json(self):
        code = "400"
        message = "message"
        target = "target"
        details = "details"

        json_data = '{"code": "400", "message": "message", "target": "target", "details": "details"}'

        test_object = ErrorResponse()
        test_object.json_deserialize(json_data)
        assert test_object
        assert test_object.code == code
        assert test_object.message == message
        assert test_object.target == target
        assert test_object.details == details

    def test_json_deserialize_from_invalid_json(self):
        json_data = '{"code": "401", "message": "message", "wrong_field": "target"}'
        test_object = ErrorResponse()

        with pytest.raises(WrongFieldError):
            assert test_object.json_deserialize(json_data)

    def test_json_serialize(self):
        code = "400"
        message = "message"
        target = "target"
        details = "details"

        test_object = ErrorResponse(
            code=code,
            message=message,
            target=target,
            details=details
        )

        serialized_data = test_object.json_serialize()
        assert serialized_data["code"] == code
        assert serialized_data["message"] == message
        assert serialized_data["target"] == target
        assert serialized_data["details"] == details
