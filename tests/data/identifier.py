class Identifier:
    PATH = "path"
    ID = "id"

    """ Identifier for the endpoints, used for the test cases. """

    """ Identifier for the MQTT recipient endpoint with a P12 certificate. """
    MQTT_RECIPIENT_P12 = {
        'path': "Mqtt/CommunicationUnit/P12/Recipient",
        'id': "dc1b27ce-c283-11ed-afa1-0242ac120002"
    }

    """ Identifier for the MQTT sender endpoint with a P12 certificate. """
    MQTT_SENDER_P12 = {
        'path': "Mqtt/CommunicationUnit/P12/Sender",
        'id': "e6bf88f0-c283-11ed-afa1-0242ac120002"
    }

    """ Identifier for the MQTT recipient endpoint with a PEM certificate. """
    MQTT_RECIPIENT_PEM = {
        'path': "Mqtt/CommunicationUnit/PEM/Recipient",
        'id': "d9786fbc-c888-11ed-afa1-0242ac120002"
    }

    """ Identifier for the MQTT sender endpoint with a PEM certificate. """
    MQTT_SENDER_PEM = {
        'path': "Mqtt/CommunicationUnit/PEM/Sender",
        'id': "fe3ab36a-ddc7-11ed-b5ea-0242ac120002"
    }

    """ Identifier for the MQTT message recipient endpoint with a PEM certificate. """
    MQTT_MESSAGE_RECIPIENT = {
        'path': "Mqtt/CommunicationUnit/Messages/Recipient",
        'id': "dde93925-b35d-4fac-9e83-a1d1ff0ff077"
    }

    """ Identifier for the MQTT message sender endpoint with a PEM certificate. """
    MQTT_MESSAGE_SENDER = {
        'path': "Mqtt/CommunicationUnit/Messages/Sender",
        'id': "e3df3eb7-c6e2-45f2-9b95-eb5300cadc56"
    }