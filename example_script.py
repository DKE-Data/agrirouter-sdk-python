from pprint import pprint

from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from agrirouter.onboarding.response import SoftwareOnboardingResponse
import time

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzGt41/+kSOTlO1sJvLIN
6RAFaOn6GiCNX/Ju0oVT4VMDHfuQMI5t9+ZgBxFmUhtY5/eykQfYJVGac/cy5xyk
F/1xpMzltK7pfo7XZpfHjkHLPUOeaHW0zE+g2vopQOARKE5LSguCBUhdtfFuiheR
IP0EU+MtEQDhlfiqYLAJkAvZHluCH9q6hawn0t/G873jlzsrXBqIgKboXqyz1lRE
SvMyqX04Xwaq1CgAZjHXBVWvbuOriCR0P2n13/nkCgBgLd/ORwVilb4GQDXkkCSg
uOVcRU3s/KG/OVJTonHVlLvDzBA5GLrpZMpzC4EfzXBM98s4Vj6IOAIQeY84Sppj
qwIDAQAB
-----END PUBLIC KEY-----"""

private_key = """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDMa3jX/6RI5OU7
Wwm8sg3pEAVo6foaII1f8m7ShVPhUwMd+5Awjm335mAHEWZSG1jn97KRB9glUZpz
9zLnHKQX/XGkzOW0rul+jtdml8eOQcs9Q55odbTMT6Da+ilA4BEoTktKC4IFSF21
8W6KF5Eg/QRT4y0RAOGV+KpgsAmQC9keW4If2rqFrCfS38bzveOXOytcGoiApuhe
rLPWVERK8zKpfThfBqrUKABmMdcFVa9u46uIJHQ/afXf+eQKAGAt385HBWKVvgZA
NeSQJKC45VxFTez8ob85UlOicdWUu8PMEDkYuulkynMLgR/NcEz3yzhWPog4AhB5
jzhKmmOrAgMBAAECggEAEEr6mUCzb+nqiWYSqxsH980CmV+Yww9YJU8V3SqqSlnK
9E9SKUSY6DrQ6Y9N9/pdBjQcY+nbpPHRnS+VO41xWMYnEisQneuZCbDJ40/ypFiD
IfFrRUkobWZlXD63Hggd5fgDkTXEmbYwXemN1WzWcOopt6PyOho3YLQupEEzqerb
XkzBFWwWO9589fbWnlaSoJPtgA8gFxeJJkU3kG10Epj6wV17yo6DuyVZpemGPTUL
uVl7yNx9O/Lp8UXRlBtSEEBQqoJaGy9mzVZyobXNKvdlZxwlkbJQpZB/m4dzqbyn
Wv+lSJdmbOnOzc67FfRqHf/irIdg6aInJd6WxZ3rPQKBgQDlxrcePlzpNwJOWtXb
sneHU50Lx73u183q5dtKlH/FudhOgP4aot6+q1KDu3b9rRakGJUKQYoLgGNwhl/7
5CF0iKQE+5JZ5R9YpwFoDuALjPfic5vFN76G851ccz5pfThLjCMV1NgKJskaefP0
OdV+UW9qOIxR8UAMntWTTrQzFwKBgQDjv+2Kz1/KsXSPaw+mJKsmUnC2YbqeAr+9
Dwm7Hr0RZWkkS2EjqcMxvq0D8bYcuJvrlZFmB/r6Ly0MKlfsUT+64LAQnKHhlCUi
vlE7VuDOR16lC4ZCPeWtjrL45fpj+Lhe54m7rCT8F+Ocdxv2yNQrSBbQ6epOVuDz
XJaSRt/AjQKBgQCrBZPIS+yFnO73eP6SLixvKhnK6dmBi1h1zK3CvfK4LZJFJBd9
pdoampOo/wAa4hjm/HD6GDvyQZZB65JHfs4z2XwTRVfx1urU5kDSvbeegUcDYr7/
NHV4JpzqcdBzXcNn359BoZFHRQUL0tdz4RP5mA1QR1SRrPnaKuKWaM8Q8wKBgQC5
mY9br+PAqxzyQ61dGETh1g1ElCAg5NyclcS4WTR7GMm2ajefeJk50MnujOx8O3XV
Zu422AoQGKH9aAR+8Teec70HzJ2f17rrtW09jm9lq4PVvK6NDSQ/bCst6z1Ce07F
CKuV5ZO+XTmAKREA7Gj7XKQ7XGU1sldf+/Q5AMkXgQKBgQC4lXL9zLV/vfWUTPSR
qlGcS2+WYtjWPapDZa+7zlxGdPgOTri4nJO69Bs9ReLlzsYKSBihfpWPxcl9sS65
KFrlBkR/vzKYjCFXB6cmMP61mUrgGQRoYJQBetAyEiXZL3zjt1R/Dndk0kHkVmHr
HjmgzBRxXFy5uph6Ue6dxyszaA==
-----END PRIVATE KEY-----"""


onboarding_response_mqtt = {
    "deviceAlternateId": "2145df0e-3451-46cb-bf23-23191af66fce",
    "capabilityAlternateId": "523e4623-68d2-43d4-a0cc-e2ada2f68b5e",
    "sensorAlternateId": "1489638c-7bed-4205-ad77-8d11efdc779f",
    "connectionCriteria": {
        "gatewayId": "2",
        "host": "dke-qa.eu10.cp.iot.sap",
        "port": 8883,
        "clientId": "2145df0e-3451-46cb-bf23-23191af66fce",
        "measures": "measures/2145df0e-3451-46cb-bf23-23191af66fce",
        "commands": "commands/2145df0e-3451-46cb-bf23-23191af66fce"
    },
    "authentication": {
        "type": "PEM",
        "secret": "JNKdNg8R0lwmFgvrUfOCc7inebr0h?!7Z9wL",
        "certificate": "-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE6zAdBgoqhkiG9w0BDAEDMA8ECMkL85F+LbPbAgMCAAAEggTI1CmRlnDUStBv\nTycvaRVFMCk1OuynhiOYRF6HBFFXBCxWKZa3WqTShLdf9iCel/NgtdZIiQsoD1LL\nMxVyh8pWAfLQ+pDJLvM6suQjHALt8dW5iTeCZ7R1gzFvPJ+xnDGFFytN7HmGSvHM\nQbcCOuEeIu8U6ENa6/+WmUwK9/ZMkLNqDHVKEGpI+lSJs8JWEE+S3Klmsxuq0dvz\nh6o3V7RKFwMfUZOQLHezGBDjLfEBdP+d2G87CY+LSzinL8pFhLwyrXFKfYWYoT0m\n5PkDdjfiVq3SJIUoQWnGrjaVVw4TV3WSxmhQnWbDwOQydr8DAiBxDMYoeK3rePpC\nwh6KATnBrovq1icqjonYDE0T+3Rs2SUbG+3+m9Zj4j46L2Sh9bUB6qxdw74Ck2/z\nAzJ1N+tB+RL7UvOpMOhmndMBl5qpx9dFFy8Z/N7w4YTQLZLN7chD8ApeFhCgvppt\nAGh8/VeWO54OC9ZOSHpxEl7sJz97jaHYNbw/lGbDk7cOZezwpA0NCWZ/Bb1vRDzy\n8EDX9s1hOA3jiy2T1RSyk2Rj/12pWdKtdSO8lMhMKC0B32Zr1F8rBJKDVzqFWuTt\nn+pXOKedyOA/ggyvYJdsltP8O4XB2oBN3WBdFK7Y1FG/tN30LsaqcnFTxab5v1Pp\ngq2dHu6Xy0TCMAw/DH3RmGXlGnDDWu86Zad7TjjrEZvpSIv4TTSCqqTvc4IN0xFX\nbKZCrY6JSkJWWnDMKrsRYOijUDvpAbYwZuTV9PAljYbt5YX778qxV9O0fNBQdaww\nNlfxU93jgr4g3E9nIzRxLu9S98hPbxKUnVYiQmYvP7vJUcUSo5F0LmUU/nvHY1pi\nr4tZDp8Xu1aZy7cOd3sTbf/68IjiZMZlF5/PVlOFOo40yGqW600j/qEqXoY/492h\nONXUCpHKaG/Pkjtg9THuYoaw1773gxYYsYLt+c6NkQCCsydOr2BMZQ4Qy4bZV67D\n2RNDeZzSBY6jEX6dnfY0FJqIsSiw28Ek5NXx0HTEGN8txPkx/1dfu3RfZnzUqT/0\nmS9xcWVYRmlip3vm48fMecqP/DNIHyjVLC39SsFdeXa+De76z/S3+or0t7HGlUim\nNVkIcWqm/sD2ia8hYberaRRTbUQ1iObNToIg8dA/xna6D61sYK8jkf1GVPpKsCTA\nOVW5u9XrE1f5YQEovE9kFgvtzs0u6jSeI9edqVadH1u6hX4QWQSTrcTb3raqAKpK\nl67cQ96eXI1WQPSdPhQPTjqzOPZDbot3qMkGFijHar7FdQjDx/cNhqhvxv0LWsvl\njgep1czUFoo1BS3wTUiO0qyloNGOQdgmlTOHbMFk1wgoNyAohfZtfn6LH/zlJnE3\nQ0YkUKgAG+1N/PmkQFO0k5qAflUV7h+HAzT1ZAZcscjHNbQFDc0Zjq9nE9sfhxE8\nOFpnF9Jp3fQVekyyC/dsCxtJdYfhxqYe+BzZu0SlsLCmc1JoK5lkiXQwv6+cFpKW\nwfHMTTrCoOetJyiF7oJX+t4adzmLmnujiw5izxObWQJ7avHC1oYNHfRejrOtlu34\n0nDPRFiSDyEbDCBXPe9dIafqjJVLQGFOeXC8/VN9cGSZp2JV8rqumWOr9E+Wd5zU\n8MRZpevo0i3rPgdyFRpw\n-----END ENCRYPTED PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\nMIIEaDCCA1CgAwIBAgIPANHZYxYlOc+wEAEDDWDpMA0GCSqGSIb3DQEBCwUAMFYx\nCzAJBgNVBAYTAkRFMSMwIQYDVQQKExpTQVAgSW9UIFRydXN0IENvbW11bml0eSBJ\nSTEiMCAGA1UEAxMZU0FQIEludGVybmV0IG9mIFRoaW5ncyBDQTAeFw0yMTExMTIw\nNzMyMjNaFw0yMjExMTIwNzMyMjNaMIG1MQswCQYDVQQGEwJERTEcMBoGA1UEChMT\nU0FQIFRydXN0IENvbW11bml0eTEVMBMGA1UECxMMSW9UIFNlcnZpY2VzMXEwbwYD\nVQQDFGhkZXZpY2VBbHRlcm5hdGVJZDoyMTQ1ZGYwZS0zNDUxLTQ2Y2ItYmYyMy0y\nMzE5MWFmNjZmY2V8Z2F0ZXdheUlkOjJ8dGVuYW50SWQ6MTExNjkwMzQ5MHxpbnN0\nYW5jZUlkOmRrZS1xYTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJeF\naxjV7Xk1R2dFjadN6WsUkrmcVu44vZRCJEbR7Chkg1xcXT6cgIlokO/V4lTgaD6i\neCMKMFegjXzEJQy0dyIWncozcmt6HJFxpdjVQtdCtDtCWykGscNDgvv5ukykOOKI\nMzWJ4d2cJRlostpNe4FYZoPp6cArSHTl9DvfYqjZ/ykeTa1w157dgVxPxezHrJMl\n+z2XgO37mq6CJLw8J6W8RBHbCADgB8c6qGHgJnBURyxnoHHi/yqdIKC6cOs8NAnc\nyVmnvLDu8RUWu9pWkqFHhMvSqdkUCTYORZ9mUTm/Kmv6ss2NaYT4uUBZTskwnAa9\nFLdj+DV2NG0OQl3NYr8CAwEAAaOB0jCBzzBIBgNVHR8EQTA/MD2gO6A5hjdodHRw\nczovL3Rjcy5teXNhcC5jb20vY3JsL1RydXN0Q29tbXVuaXR5SUkvU0FQSW9UQ0Eu\nY3JsMAwGA1UdEwEB/wQCMAAwJQYDVR0SBB4wHIYaaHR0cDovL3NlcnZpY2Uuc2Fw\nLmNvbS9UQ1MwDgYDVR0PAQH/BAQDAgbAMB0GA1UdDgQWBBSRf8DUjowgQ+6amVIs\njd7zM7VWqjAfBgNVHSMEGDAWgBSVt7P1WN7VtLNYRuDypsl4Tr0tdTANBgkqhkiG\n9w0BAQsFAAOCAQEARzSc9GLpSU3pRJPIfgadHrZ+2KQsPsQ1/fLlASlt4V1Rlxn7\n/tn0gk3sP0X5/TrkO+N0kx1qrLarxWSDiVfaXoPa6Lit30SBPnPLUPPPZeTJOz5r\nTW9PkPPuC39GlM1biVoil2cLZrTr9DMSUoBvR4IVKQoJveQsLwn7Ea+SDPE0uvZV\nbDN6UPGZ2yIiCXO1MODJ6r3A4EDD2MArGgfhGdbvJNAY36ShFJhzfzi0t8linEAA\nxh0vcaEEIkVeEiwiguyGWB69X88cjZ0Q5cCf0r6iu3oQnB57uM5TW12OwXQN1NpQ\neK3EMFSoM6BYJu/3B8TXhNmpNBvD7KYozw9XaA==\n-----END CERTIFICATE-----\n"
    }
}




import agrirouter as ar
from agrirouter.onboarding.enums import GateWays
from agrirouter.messaging.enums import CapabilityType
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.messaging.services.commons import HttpMessagingService, MqttMessagingService
from agrirouter import ListEndpointsParameters, ListEndpointsService, SubscriptionService, SubscriptionParameters
from agrirouter.utils.uuid_util import new_uuid


application_id = "8c947a45-c57d-42d2-affc-206e21d63a50"		# # store here your application id. You can find it in AR UI


def example_auth():
    print("Authorization...\n")

    auth_params = ar.AuthUrlParameter(application_id=application_id, response_type="onboard")
    auth_client = ar.Authorization("QA", public_key=public_key, private_key=private_key)
    auth_url = auth_client.get_auth_request_url(
        auth_params)  # use this url to authorize the user as described at https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/integration/authorization.html#perform-authorization
    print(f"auth_url={auth_url}")

    auth_result_url = input(
        "Enter auth_url (the url the user was redirected to after his authorization, see above): ")  # the url the user was redirected to after his authorization.
    auth_response = auth_client.extract_auth_response(
        auth_result_url)  # auth_response contains the results of the auth process
    auth_client.verify_auth_response(auth_response)  # you may verify auth_response to ensure answer was from AR

    print(
        f"auth_response is successful: {auth_response.is_successful}")  # True if user accepted application, False if he rejected

    print(
        f"auth_response is valid: {auth_response.is_valid}")  # Result of verification, if False, response was not validated by public key. Doesn't indicate the auth was successfull. Accessible only after response verifying

    # Get dict containing data from auth process you will use for futher communication.
    # If auth was rejected, contains {"error"} key.
    # If auth was accepted, contains {signature, state, token, credentials{account, expires, regcode}} keys
    # Even if response verifying was not processed or failed, the results will be returned. But in that case you act on your risk.
    auth_data = auth_response.get_auth_result()
    print(f"auth_data: {auth_data}")

    return auth_data


def example_onboarding(gateway_id):

    auth_data = example_auth()

    print("Onboarding...\n")

    id_ = "urn:myapp:snr00003234"  # just unique
    certification_version_id = "edd5d6b7-45bb-4471-898e-ff9c2a7bf56f"  # get from AR UI
    time_zone = "+03:00"

    onboarding_client = ar.SoftwareOnboarding("QA", public_key=public_key, private_key=private_key)
    onboarding_parameters = ar.SoftwareOnboardingParameter(id_=id_, application_id=application_id,
                                                           certification_version_id=certification_version_id,
                                                           gateway_id=gateway_id, time_zone=time_zone,
                                                           reg_code=auth_data.get_decoded_token().regcode)
    onboarding_verifying_response = onboarding_client.verify(onboarding_parameters)
    print(f"onboarding_verifying_response.status_code: {onboarding_verifying_response.status_code}")
    print(f"onboarding_verifying_response.text: {onboarding_verifying_response.text}")
    onboarding_response = onboarding_client.onboard(onboarding_parameters)
    print(f"onboarding_response.status_code: {onboarding_response.status_code}")
    print(f"onboarding_response.text: {onboarding_response.text}")

    return onboarding_response


def example_list_endpoints_mqtt(onboarding_response_data, foo):
    onboarding_response = SoftwareOnboardingResponse()
    onboarding_response.json_deserialize(onboarding_response_data)

    messaging_service = MqttMessagingService(
        onboarding_response=onboarding_response,
        on_message_callback=foo

    )
    list_endpoint_parameters = ListEndpointsParameters(
        technical_message_type=CapabilityType.ISO_11783_TASKDATA_ZIP.value,
        direction=ListEndpointsQuery.Direction.Value("SEND_RECEIVE"),
        filtered=False,
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    list_endpoint_service = ListEndpointsService(messaging_service)

    messaging_result = list_endpoint_service.send(list_endpoint_parameters)
    print("Sent message: ", messaging_result)

    # Is needed for waiting of messaging responses from outbox
    while True:
        time.sleep(1)


def example_list_endpoints_http(onboarding_response_data):
    onboarding_response = SoftwareOnboardingResponse()
    onboarding_response.json_deserialize(onboarding_response_data)

    messaging_service = HttpMessagingService()
    list_endpoint_parameters = ListEndpointsParameters(
        technical_message_type=CapabilityType.ISO_11783_TASKDATA_ZIP.value,
        direction=2,
        filtered=False,
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    list_endpoint_service = ListEndpointsService(messaging_service)

    messaging_result = list_endpoint_service.send(list_endpoint_parameters)
    print("Sent message: ", messaging_result)

    return messaging_result


def example_subscription_http(onboarding_response_data):
    onboarding_response = SoftwareOnboardingResponse()
    onboarding_response.json_deserialize(onboarding_response_data)

    messaging_service = HttpMessagingService()
    subscription_service = SubscriptionService(messaging_service)
    tmt = CapabilityType.ISO_11783_TASKDATA_ZIP.value
    subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=tmt)
    subscription_parameters = SubscriptionParameters(
        subscription_items=[subscription_item],
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )

    messaging_result = subscription_service.send(subscription_parameters)
    print("Sent message: ", messaging_result)

    return messaging_result


def example_subscription_mqtt(onboarding_response_data, on_msg_callback):
    onboarding_response = SoftwareOnboardingResponse()
    onboarding_response.json_deserialize(onboarding_response_data)

    messaging_service = MqttMessagingService(onboarding_response, on_message_callback=on_msg_callback)
    subscription_service = SubscriptionService(messaging_service)
    tmt = CapabilityType.ISO_11783_TASKDATA_ZIP.value
    subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=tmt)
    subscription_parameters = SubscriptionParameters(
        subscription_items=[subscription_item],
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )

    messaging_result = subscription_service.send(subscription_parameters)
    print("Sent message: ", messaging_result)

    # Is needed for waiting of messaging responses from outbox
    while True:
        time.sleep(1)


def on_message_callback(client, userdata, msg):

    # Define here the way receiving messages will be processed

    from agrirouter.messaging.decode import decode_response
    from agrirouter.messaging.decode import decode_details
    from agrirouter.messaging.messages import OutboxMessage

    outbox_message = OutboxMessage()
    outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))

    print(outbox_message.command.message)

    decoded_message = decode_response(outbox_message.command.message)
    print(decoded_message.response_envelope)

    try:
        decoded_details = decode_details(decoded_message.response_payload.details)
        print(decoded_details)
    except:
        pass


if __name__ == "__main__":
    onboarding_response_mqtt = example_onboarding(GateWays.MQTT.value)
    example_list_endpoints_mqtt(onboarding_response_mqtt.json_serialize(), on_message_callback)

    # of for http
    onboarding_response_mqtt = example_onboarding(GateWays.REST.value)
    example_list_endpoints_http(onboarding_response_mqtt.json_serialize())
