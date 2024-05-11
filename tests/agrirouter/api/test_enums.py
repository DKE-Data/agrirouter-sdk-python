import unittest

import pytest

from src.agrirouter.api.enums import BaseEnum


class TestEnum(BaseEnum):
    VALUE1 = 'value1'
    VALUE2 = 'value2'


class TestBaseEnum(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.enum = TestEnum

    def test_choices(self):
        expected_choices = [('value1', 'VALUE1'), ('value2', 'VALUE2')]
        assert self.enum.choices() == expected_choices

    def test_values_list(self):
        expected_values_list = ['value1', 'value2']
        assert self.enum.values_list() == expected_values_list
