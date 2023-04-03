class Identifier:
    PATH = "path"
    ID = "id"

    """ Identifier for the endpoints, used for the test cases. """

    """ Identifier for the HTTP recipient endpoint with a P12 certificate. """
    HTTP_RECIPIENT_P12 = {
        'path': "Http/CommunicationUnit/P12/Recipient",
        'id': "646a1f40-c275-11ed-afa1-0242ac120002"
    }

    """ Identifier for the HTTP sender endpoint with a P12 certificate. """
    HTTP_SENDER_P12 = {
        'path': "Http/CommunicationUnit/P12/Sender",
        'id': "6bd7796c-c275-11ed-afa1-0242ac120002"
    }

    """ Identifier for the HTTP recipient endpoint with a PEM certificate. """
    HTTP_RECIPIENT_PEM = {
        'path': "Http/CommunicationUnit/PEM/Recipient",
        'id': "e5b9de9a-c889-11ed-afa1-0242ac120002"
    }

    """ Identifier for the HTTP sender endpoint with a PEM certificate. """
    HTTP_SENDER_PEM = {
        'path': "Http/CommunicationUnit/PEM/Sender",
        'id': "e9b0d99a-c889-11ed-afa1-0242ac120002"
    }

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

    """ Identifier for the MQTT sender endpoint with a P12 certificate. """
    MQTT_SENDER_PEM = {
        'path': "Mqtt/CommunicationUnit/PEM/Sender",
        'id': "083d2374-c889-11ed-afa1-0242ac120002"
    }
