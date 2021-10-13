from agrirouter.auth.enums import BaseEnum


class CertificateTypes(BaseEnum):
    PEM = "PEM"
    P12 = "P12"


class GateWays(BaseEnum):
    MQTT = "2"
    REST = "3"
