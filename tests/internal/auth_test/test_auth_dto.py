"""Tests src/auth/dto.py"""
import pytest

from src.auth.dto import AuthorizationToken
from src.api.exceptions import WrongField


class TestAuthorizationToken:
    def test_json_deserialize_from_valid_dict(self):
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

    def test_json_deserialize_from_invalid_dict(self):
        account = "account"
        regcode = "regcode"
        expires = "01-01-2021"
        test_object = AuthorizationToken()

        with pytest.raises(WrongField):
            test_object.json_deserialize({"regcode": regcode, "expires": expires, "wrong_key": account})

    def test_json_deserialize_from_valid_json(self):
        account = "account"
        regcode = "regcode"
        expires = "01-01-2021"

        json_data = '{"account": "account", "regcode": "regcode", "expires": "01-01-2021"}'

        test_object = AuthorizationToken()
        test_object.json_deserialize(json_data)
        assert test_object
        assert test_object.account == account
        assert test_object.regcode == regcode
        assert test_object.expires == expires

    def test_json_deserialize_from_invalid_json(self):
        json_data = '{"account": "account", "regcode": "regcode", "wrong_key": "01-01-2021"}'
        test_object = AuthorizationToken()

        with pytest.raises(WrongField):
            assert test_object.json_deserialize(json_data)
