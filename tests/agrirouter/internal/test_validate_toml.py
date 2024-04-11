import toml


class TestTomlValidation:

    def test_validate_toml(self):
        toml.load("../../../pyproject.toml")
        pass
