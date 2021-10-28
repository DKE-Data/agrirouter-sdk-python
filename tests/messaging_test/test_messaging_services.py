import pytest
from google.protobuf.timestamp_pb2 import Timestamp

from agrirouter import CapabilityParameters, CapabilityService, QueryHeaderService, QueryHeaderParameters
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod

from agrirouter.messaging.builders import CapabilityBuilder
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.services.commons import HttpMessagingService
from agrirouter.messaging.services.http.outbox import OutboxService
from agrirouter.onboarding.response import SoftwareOnboardingResponse
from agrirouter.utils.uuid_util import new_uuid
from tests.sleeper import let_agrirouter_process_the_message

onboarding_response = SoftwareOnboardingResponse()
onboarding_response.json_deserialize('{"deviceAlternateId":"e2b512f3-9930-4461-b35f-2cdcc7f017fd","capabilityAlternateId":"523e4623-68d2-43d4-a0cc-e2ada2f68b5e","sensorAlternateId":"185cd97b-ed0b-4e75-a6e2-6be1cdd38a06","connectionCriteria":{"gatewayId":"3","measures":"https://dke-qa.eu10.cp.iot.sap/iot/gateway/rest/measures/e2b512f3-9930-4461-b35f-2cdcc7f017fd","commands":"https://dke-qa.eu10.cp.iot.sap/iot/gateway/rest/commands/e2b512f3-9930-4461-b35f-2cdcc7f017fd"},"authentication":{"type":"PEM","secret":"VXHfXV7g#3COYT1Q5YkTxrRXo1IjdN8xSZ3O","certificate":"-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE6zAdBgoqhkiG9w0BDAEDMA8ECHlX0q4qf0tSAgMCAAAEggTI4XIOXehAN02J\nwUrHPe2BCGEqXvyA2QzWMBkqYRm7dCmhL/ay1JzJkkDf2afS/1FE0Sl3So1AMKBe\nhpqZUpaz5g7tN1ktl9BReXC+pptJPpy3XSpZ/8Bg3Jje4eYn2aCWMSNbnw0SO9Sf\nZnUZrNwQH9GSR35fGHYPaYHmAIM9axaUSn6/LfsrifdORY38r9EKvrcuIYFJ18ai\ngHoCAboaPLY52m/UkaM0WNnpTrHm/72G8978jpZKYZmbmp7/qdB7+aQ+WZWs4u/V\nCR6vzgkyWaFzQK5GMKCMBgHteq5900FY9Iz/ZBS/gyoHoVdMsRKRBSXfNebdvADC\nkksZBfaYqMI58CFEuVODi7gD+YKcu7/5BjX8DJ72eDFaYa1ZIC+na24gel8x85UF\n+TwFSQ4NgHmqcUkZJOyRtcnMREP79ZkdGXi4l6eZk4hG9KhfM66HgcvIzGT6e1SF\nJrKcLTVYUdYSyhLZmk7DflgI5VoCKX1/P1O0iiyWqsbqhjfsnfTpaCaveMb+c/2z\nSaw3tc5G6th/QdN72wZTM1Vqb4562JEpxvkxY4i2PW1Ky9HNY0M+jy0DL/KhfnM9\nm8abxdgILTu3WcxnfH7f8uiK2R9zgnIf+CCDtGGWftOGgV5MY4t0XLAsGSadNdqH\nrpTguI4XMcQET0ZEE7fTbkvJ2+QVWz3vD8w4/ryZx12ZzQCoewd5nPQD/JgLoo2R\n8Pdp2TQDYrn0PYZHus1GnPL7kAs34gl1zFNxFF8nYSSP0hITc2zWm8XuLyMc8fgs\nymXZPdTz9LQZPqs5t+P0gL04xegaXiYWWAhZFkMx9/0+zeoNK+w28cTsLRC4oQcJ\nkaq69f7gHIg3ar75Zzzc1xUEgz50oJI2BCDVLllHzoAWFjl5t/9hGcBirP3QOKwg\nCKfHKnbLkSS+2omhp3zBecX7moDS6+RcMMIUvMbHHLx8l4uv/cDtWIh++I21hzQu\ntSaIK6gglGE0OZJN3tPmy3CdHqbapBWvfCMGD2J2xISJCoSwmR58fni4pyniTydt\nJH040YpDUuUxIDlVTFAsmMRm5vh2KkE4DVr1UqA+JJgHRuQiuVbprm/QU2bumTG+\n4vhOKcaSgbQW3++NtvfVSymz5/IJXOMQIzprokvC+6GwiRUBIov7angWwUB9X5iC\nN0rfJ5MbNkabXsFRQpbXYV7z/P+t/9A8A5LBr+DiPLib9i3WI4sHV5aLZapJ3R4u\neBCVB+VIGbcTM19t51h4ohZhY2Q9CYXVnle7ol0Nz/mUiX0Az9oF6GQCngMFdqMh\nftl2XdCq43AZA7hHP+wqKkjOo7i5Lr0IRWw5F7IexV8mHDwx560DJkp0bZM9+UxA\nu1JcTLDJR+a/aOsx5CDSWig+W3XNCQfC4kVhNUlWZ1yQ8Heh+NB3kD+Krvby40DL\nzNOe6VSkFCjKn2st1yJkdcdhLs8mPE1DEk7WRFS+AMaIgXIGpdoBIlUwHpwP7djd\n8gC9e3kFTAazudZkTCi8QnhAeH1coxVhB6+WbzVnFzJDZuy65DiVDSmOjlHmxF7A\nZc5LCo1vmtER3d08bjuz+33dCGS2yKg2Q7Nd3rymUlGzPEx+dPFmvXaDWNXghdbj\nc9PfhpiX5tt83tHe7E2C\n-----END ENCRYPTED PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\nMIIEaTCCA1GgAwIBAgIQAPktOgtD/4tlEAEHAL6qbTANBgkqhkiG9w0BAQsFADBW\nMQswCQYDVQQGEwJERTEjMCEGA1UEChMaU0FQIElvVCBUcnVzdCBDb21tdW5pdHkg\nSUkxIjAgBgNVBAMTGVNBUCBJbnRlcm5ldCBvZiBUaGluZ3MgQ0EwHhcNMjExMDI1\nMTk0MzE1WhcNMjIxMDI1MTk0MzE1WjCBtTELMAkGA1UEBhMCREUxHDAaBgNVBAoT\nE1NBUCBUcnVzdCBDb21tdW5pdHkxFTATBgNVBAsTDElvVCBTZXJ2aWNlczFxMG8G\nA1UEAxRoZGV2aWNlQWx0ZXJuYXRlSWQ6ZTJiNTEyZjMtOTkzMC00NDYxLWIzNWYt\nMmNkY2M3ZjAxN2ZkfGdhdGV3YXlJZDozfHRlbmFudElkOjExMTY5MDM0OTB8aW5z\ndGFuY2VJZDpka2UtcWEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCY\nRAKTeVe2Eo4EtV1QJi1m3gZDpAAXYYhGo8905yw4XZD9M2fCyMbUVcoAm/5lGN+W\nsMk/GsfNeBRmd80SLv6/Z7342tVryhslkGL0TVw2MHMw+1cEAPsH6EthrvH6poTs\ngGDtUB4ad2BOvBwveTPpHwdWxyDUvb74mXwXZ9XgIo/VJKSEr6DlO+zv52BUXRh9\nS70m4dgM0aTM/iRYITrPPXHZfY91M9lsypp64m1dHzDXiQaWvFqaiyIOw/IO2V+O\nMmz3U1Q6L/8ai4WNeTTX69hprOPDTCG5WLdnDviK9hx1w6tOyRdKun7LpklZ14Rv\nApZXATxFwxrNQm2iiFbfAgMBAAGjgdIwgc8wSAYDVR0fBEEwPzA9oDugOYY3aHR0\ncHM6Ly90Y3MubXlzYXAuY29tL2NybC9UcnVzdENvbW11bml0eUlJL1NBUElvVENB\nLmNybDAMBgNVHRMBAf8EAjAAMCUGA1UdEgQeMByGGmh0dHA6Ly9zZXJ2aWNlLnNh\ncC5jb20vVENTMA4GA1UdDwEB/wQEAwIGwDAdBgNVHQ4EFgQUDG1OiFv4Ohku4sG+\n6vC9+x3nCGQwHwYDVR0jBBgwFoAUlbez9Vje1bSzWEbg8qbJeE69LXUwDQYJKoZI\nhvcNAQELBQADggEBADgzaWG5+ch1iQ6tHOHO8/sVBpQJ0kEnHCxDeJ1WRL6Qas/n\nMZPMwzmllsUhQv93fVElGosy2sMjCanCLnCh8qwb85vq7exEZBccbmUo6Epqz9XO\n/NJ4Fr1OWLtE9svRM5s0QEB6B9oQ1OjZtdjeGI9/uQSJgmzYKdI/HAFkTTugokRU\nkyr+rM6Rv9KCNbkzoNTRS6xDNs64FxEw53FBYitmtnsgXAdWPjHpkoZFIntstuFr\nVwpdxeH1TZmdvwhtImibcqGHgUqa7r1lySbK+sEdFzQcf7Ea1dRJR3r1ZfG1/ALn\nRInsXoCBNxyllk6ExpQWiczLiOY5jXnQulX51+k=\n-----END CERTIFICATE-----\n"}}')
account_id = "fb2921de-592a-49ba-be5e-94044430bc96"
certification_version_id = "edd5d6b7-45bb-4471-898e-ff9c2a7bf56f"
application_id = "8c947a45-c57d-42d2-affc-206e21d63a50"


def test_given_task_data_capabilities_capability_service_http():
    messaging_service = HttpMessagingService()
    capability_parameters = CapabilityParameters(
        application_id=application_id,
        certification_version_id=certification_version_id,
        enable_push_notification=1,
        capability_parameters=CapabilityBuilder().with_task_data(2).build(),
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    capability_service = CapabilityService(messaging_service)
    messaging_result = capability_service.send(capability_parameters)
    assert messaging_result.get_messages_ids()
    assert 1 == len(messaging_result.get_messages_ids())


# def test_list_endpoint_service_http():
#     messaging_service = HttpMessagingService()
#     list_endpoint_parameters = ListEndpointsParameters(
#         technical_message_type=CapabilityType.ISO_11783_TASKDATA_ZIP.value,
#         direction=ListEndpointsQuery.Direction.Value("SEND_RECEIVE"),
#         filtered=False,
#         onboarding_response=onboarding_response,
#         application_message_id=new_uuid(),
#         application_message_seq_no=1,
#     )
#     list_endpoint_service = ListEndpointsService(messaging_service)
#     messaging_result = list_endpoint_service.send(list_endpoint_parameters)
#     return messaging_result
#
#
# def test_list_endpoint_service_mqtt():
#     client = MqttClient(on_message_callback=foo, client_id="fb2921de-592a-49ba-be5e-94044430bc96")
#     messaging_service = MqttMessagingService(onboarding_response, client)
#     list_endpoint_parameters = ListEndpointsParameters(
#         technical_message_type=CapabilityType.ISO_11783_TASKDATA_ZIP.value,
#         direction=ListEndpointsQuery.Direction.Value("SEND_RECEIVE"),
#         filtered=False,
#         onboarding_response=onboarding_response,
#         application_message_id=new_uuid(),
#         application_message_seq_no=1,
#     )
#     list_endpoint_service = ListEndpointsService(messaging_service)
#     messaging_result = list_endpoint_service.send(list_endpoint_parameters)
#     return messaging_result
#
#
# def test_valid_subscription_service_http():
#     messaging_service = HttpMessagingService()
#     subscription_service = SubscriptionService(messaging_service)
#     items = []
#     for tmt in [CapabilityType.DOC_PDF.value, CapabilityType.ISO_11783_TASKDATA_ZIP.value]:
#         subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=tmt)
#         items.append(subscription_item)
#     subscription_parameters = SubscriptionParameters(
#         subscription_items=items,
#         onboarding_response=onboarding_response,
#         application_message_id=new_uuid(),
#         application_message_seq_no=1,
#     )
#     messaging_result = subscription_service.send(subscription_parameters)
#     return messaging_result


def test_query_header_message_http():
    messaging_service = HttpMessagingService()
    query_header_service = QueryHeaderService(messaging_service)
    sent_from = Timestamp()
    sent_to = Timestamp()
    validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)
    query_header_parameters = QueryHeaderParameters(
        message_ids=[new_uuid(), new_uuid()],
        senders=[new_uuid(), new_uuid()],
        validity_period=validity_period,
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    messaging_result = query_header_service.send(query_header_parameters)
    return messaging_result


def test_given_validity_and_missing_messages_query_messages_service_http():
    messaging_service = HttpMessagingService()
    query_header_service = QueryHeaderService(messaging_service)
    sent_from = Timestamp()
    sent_to = Timestamp()
    validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)
    query_header_parameters = QueryHeaderParameters(
        validity_period=validity_period,
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    messaging_result = query_header_service.send(query_header_parameters)
    assert messaging_result.get_messages_ids()
    assert 1 == len(messaging_result.get_messages_ids())

    let_agrirouter_process_the_message()

    outbox_service = OutboxService()
    outbox_response = outbox_service.fetch(onboarding_response)
    assert 200 == outbox_response.status_code

    messages = outbox_response.messages
    assert len(messages) == 1
    assert messages[0].command.message

    decoded_message = decode_response(outbox_response.messages[0].command.message)
    assert 204 == decoded_message.response_envelope.response_code

    decoded_details = decode_details(decoded_message.response_payload.details)
    assert decoded_details

    query_metrics = decoded_details.query_metrics
    assert 0 == query_metrics.total_messages_in_query


def test_given_invalid_sender_id_query_messages_service_http():
    messaging_service = HttpMessagingService()
    query_header_service = QueryHeaderService(messaging_service)
    query_header_parameters = QueryHeaderParameters(
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    messaging_result = query_header_service.send(query_header_parameters)
    assert messaging_result.get_messages_ids()
    assert 1 == len(messaging_result.get_messages_ids())

    let_agrirouter_process_the_message()

    outbox_service = OutboxService()
    outbox_response = outbox_service.fetch(onboarding_response)
    assert 200 == outbox_response.status_code

    messages = outbox_response.messages
    assert len(messages) == 1
    assert messages[0].command.message

    decoded_message = decode_response(outbox_response.messages[0].command.message)
    assert 204 == decoded_message.response_envelope.response_code

    decoded_details = decode_details(decoded_message.response_payload.details)
    assert decoded_details

    query_metrics = decoded_details.query_metrics
    assert 0 == query_metrics.total_messages_in_query


def test_given_invalid_message_id_query_messages_service_http():
    messaging_service = HttpMessagingService()
    query_header_service = QueryHeaderService(messaging_service)
    query_header_parameters = QueryHeaderParameters(
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    messaging_result = query_header_service.send(query_header_parameters)
    assert messaging_result.get_messages_ids()
    assert 1 == len(messaging_result.get_messages_ids())

    let_agrirouter_process_the_message()

    outbox_service = OutboxService()
    outbox_response = outbox_service.fetch(onboarding_response)
    assert 200 == outbox_response.status_code

    messages = outbox_response.messages
    assert len(messages) == 1
    assert messages[0].command.message

    decoded_message = decode_response(outbox_response.messages[0].command.message)
    assert 204 == decoded_message.response_envelope.response_code

    decoded_details = decode_details(decoded_message.response_payload.details)
    assert decoded_details

    query_metrics = decoded_details.query_metrics
    assert 0 == query_metrics.total_messages_in_query


def test_given_missing_filter_criteria_id_query_messages_service_http():
    messaging_service = HttpMessagingService()
    query_header_service = QueryHeaderService(messaging_service)
    query_header_parameters = QueryHeaderParameters(
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    messaging_result = query_header_service.send(query_header_parameters)
    assert messaging_result.get_messages_ids()
    assert 1 == len(messaging_result.get_messages_ids())

    let_agrirouter_process_the_message()

    outbox_service = OutboxService()
    outbox_response = outbox_service.fetch(onboarding_response)
    assert 200 == outbox_response.status_code

    messages = outbox_response.messages
    assert len(messages) == 1
    assert messages[0].command.message

    decoded_message = decode_response(outbox_response.messages[0].command.message)
    assert 400 == decoded_message.response_envelope.response_code

    decoded_details = decode_details(decoded_message.response_payload.details)
    assert decoded_details

    assert 1 == len(decoded_details.messages)

    for message in decoded_details.messages:
        assert "VAL_000017" == message.message_code
        assert message.message == "Query does not contain any filtering criteria: messageIds, senders or validityPeriod. Information required to process message is missing or malformed."
