import os
import tempfile

from agrirouter.service.dto.response.messaging import OnboardResponse


class CertificationService:

    @staticmethod
    def create_certificate_file_from_pen(onboard_response: OnboardResponse):
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
