from src.agrirouter.api.enums import BaseEnum


class CertificateTypes(BaseEnum):
    PEM = "PEM"
    P12 = "P12"


class Gateways(BaseEnum):
    MQTT = "2"
    HTTP = "3"
