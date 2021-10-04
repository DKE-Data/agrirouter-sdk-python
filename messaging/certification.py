import json
from pathlib import Path

from onboarding.response import BaseOnboardingResonse


def create_certificate_file(onboard_response: BaseOnboardingResonse=None, dir: Path=None):
    dir = dir if dir else Path().cwd().absolute()
    if isinstance(dir, Path):
        if dir.is_absolute():
            filename = onboard_response.get_sensor_alternate_id()
            filepath = dir.with_name(filename)
            if not filepath.exists():
                filepath.touch()
                data = onboard_response.get_authentication()["certificate"]
                filepath.write_text(json.dumps(data))

            return filepath
        raise ValueError("Invalid dir parameter. Dir must be an absolute path")
    raise ValueError("Invalid dir parameter. Must be an instance of pathlib.Path() class")
