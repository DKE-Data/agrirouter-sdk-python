import os
import tempfile


from agrirouter.onboarding.response import SoftwareOnboardingResponse


def create_certificate_file_from_pen(onboard_response: SoftwareOnboardingResponse):

    dir_ = tempfile.mkdtemp()
    prefix = onboard_response.get_sensor_alternate_id()
    data = onboard_response.get_authentication().get_certificate()
    fd, path = tempfile.mkstemp(dir=dir_, prefix=prefix, text=True)
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(data)
    except Exception as exc:
        os.remove(path)
        raise exc

    return path
