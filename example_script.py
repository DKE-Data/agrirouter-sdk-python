from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery

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


import agrirouter as ar
from agrirouter.onboarding.enums import GateWays
from agrirouter.messaging.enums import CapabilityType
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.messaging.services.commons import HttpMessagingService, MqttMessagingService
from agrirouter import ListEndpointsParameters, ListEndpointsService, SubscriptionService, SubscriptionParameters
from agrirouter.utils.uuid_util import new_uuid


application_id = "8c947a45-c57d-42d2-affc-206e21d63a50"		# # store here your application id. You can find it in AR UI


def test_auth():
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


def test_onboarding(gateway_id):

    auth_data = test_auth()

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


def test_list_endpoints_mqtt(onboarding_response):
    messaging_service = MqttMessagingService(
        onboarding_response=onboarding_response
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
    return messaging_result


def test_list_endpoint_http(onboarding_response):
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
    return messaging_result


def test_subscription_http(onboarding_response):
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
    return messaging_result


if __name__ == "__main__":
    test_list_endpoints_mqtt(test_onboarding(GateWays.MQTT.value))
