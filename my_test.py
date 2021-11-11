import os
import uuid
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from agrirouter import ListEndpointsParameters, ListEndpointsService, SubscriptionParameters, SubscriptionService, \
    RevokingParameter, Revoking, CapabilityService, CapabilityParameters, QueryHeaderService, QueryHeaderParameters
from agrirouter.auth.auth import Authorization
from agrirouter.auth.parameters import AuthUrlParameter
from agrirouter.constants.media_types import ContentTypes
from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.messaging.builders import CapabilityBuilder
from agrirouter.messaging.clients.http import HttpClient
from agrirouter.messaging.clients.mqtt import MqttClient
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.services.commons import HttpMessagingService, MqttMessagingService
from agrirouter.messaging.services.http.outbox import OutboxService
from agrirouter.onboarding.onboarding import SoftwareOnboarding
from agrirouter.onboarding.parameters import SoftwareOnboardingParameter
from agrirouter.utils.utc_time_util import now_as_utc_str
from agrirouter.utils.uuid_util import new_uuid

application_id = os.getenv("APPLICATION_ID", "8c947a45-c57d-42d2-affc-206e21d63a50")
ENV = os.getenv("ENVIRONMENT", "QA")
auth_result_url = "http://fuf.me/?state=99298901-2cbc-4f51-a0c2-3905e277e921&token=eyJhY2NvdW50IjoiZmIyOTIxZGUtNTkyYS00OWJhLWJlNWUtOTQwNDQ0MzBiYzk2IiwicmVnY29kZSI6IjBkMDE3NmU4NmYiLCJleHBpcmVzIjoiMjAyMS0xMC0xMlQxMzo0MjozNy40ODZaIn0%3D&signature=qeHHDV9sE6DxqcwoXm453Hbq7pJ92pWGUXwp3A13xtaNftjLX%2Ffcu8iiGV6%2Fu22g856Bw21Bxlrtyj2wCIm%2FJSmztYeitsfd99o5oSzPQ3zqm4tdDLH8qvnONRJqck7OWChVU4mArk14uVQv2ofxANGogspp1T1k51WLtPtoHBxFu6XAS3Cbm%2FpkakqalR%2FnWjAsCIlf9vGvX6oQnSX2lUDYmMCNNvzLwHYPCQgwF1vusbXE%2BAxwpBAFnZHFHPmjbTVUPXF6Hxb%2B3plwwm4tfXK9%2B7dwkZvUbKgIkcq2AYKFSTKwAns7hBjFSt6uhWK17%2Brzc%2FsarW30CZ%2BIGuuQeQ%3D%3D"
private_key = os.getenv("PRIVATE_KEY",
                        "-----BEGIN PRIVATE KEY-----\n"
                        "MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDMa3jX/6RI5OU7\n"
                        "Wwm8sg3pEAVo6foaII1f8m7ShVPhUwMd+5Awjm335mAHEWZSG1jn97KRB9glUZpz\n"
                        "9zLnHKQX/XGkzOW0rul+jtdml8eOQcs9Q55odbTMT6Da+ilA4BEoTktKC4IFSF21\n"
                        "8W6KF5Eg/QRT4y0RAOGV+KpgsAmQC9keW4If2rqFrCfS38bzveOXOytcGoiApuhe\n"
                        "rLPWVERK8zKpfThfBqrUKABmMdcFVa9u46uIJHQ/afXf+eQKAGAt385HBWKVvgZA\n"
                        "NeSQJKC45VxFTez8ob85UlOicdWUu8PMEDkYuulkynMLgR/NcEz3yzhWPog4AhB5\n"
                        "jzhKmmOrAgMBAAECggEAEEr6mUCzb+nqiWYSqxsH980CmV+Yww9YJU8V3SqqSlnK\n"
                        "9E9SKUSY6DrQ6Y9N9/pdBjQcY+nbpPHRnS+VO41xWMYnEisQneuZCbDJ40/ypFiD\n"
                        "IfFrRUkobWZlXD63Hggd5fgDkTXEmbYwXemN1WzWcOopt6PyOho3YLQupEEzqerb\n"
                        "XkzBFWwWO9589fbWnlaSoJPtgA8gFxeJJkU3kG10Epj6wV17yo6DuyVZpemGPTUL\n"
                        "uVl7yNx9O/Lp8UXRlBtSEEBQqoJaGy9mzVZyobXNKvdlZxwlkbJQpZB/m4dzqbyn\n"
                        "Wv+lSJdmbOnOzc67FfRqHf/irIdg6aInJd6WxZ3rPQKBgQDlxrcePlzpNwJOWtXb\n"
                        "sneHU50Lx73u183q5dtKlH/FudhOgP4aot6+q1KDu3b9rRakGJUKQYoLgGNwhl/7\n"
                        "5CF0iKQE+5JZ5R9YpwFoDuALjPfic5vFN76G851ccz5pfThLjCMV1NgKJskaefP0\n"
                        "OdV+UW9qOIxR8UAMntWTTrQzFwKBgQDjv+2Kz1/KsXSPaw+mJKsmUnC2YbqeAr+9\n"
                        "Dwm7Hr0RZWkkS2EjqcMxvq0D8bYcuJvrlZFmB/r6Ly0MKlfsUT+64LAQnKHhlCUi\n"
                        "vlE7VuDOR16lC4ZCPeWtjrL45fpj+Lhe54m7rCT8F+Ocdxv2yNQrSBbQ6epOVuDz\n"
                        "XJaSRt/AjQKBgQCrBZPIS+yFnO73eP6SLixvKhnK6dmBi1h1zK3CvfK4LZJFJBd9\n"
                        "pdoampOo/wAa4hjm/HD6GDvyQZZB65JHfs4z2XwTRVfx1urU5kDSvbeegUcDYr7/\n"
                        "NHV4JpzqcdBzXcNn359BoZFHRQUL0tdz4RP5mA1QR1SRrPnaKuKWaM8Q8wKBgQC5\n"
                        "mY9br+PAqxzyQ61dGETh1g1ElCAg5NyclcS4WTR7GMm2ajefeJk50MnujOx8O3XV\n"
                        "Zu422AoQGKH9aAR+8Teec70HzJ2f17rrtW09jm9lq4PVvK6NDSQ/bCst6z1Ce07F\n"
                        "CKuV5ZO+XTmAKREA7Gj7XKQ7XGU1sldf+/Q5AMkXgQKBgQC4lXL9zLV/vfWUTPSR\n"
                        "qlGcS2+WYtjWPapDZa+7zlxGdPgOTri4nJO69Bs9ReLlzsYKSBihfpWPxcl9sS65\n"
                        "KFrlBkR/vzKYjCFXB6cmMP61mUrgGQRoYJQBetAyEiXZL3zjt1R/Dndk0kHkVmHr\n"
                        "HjmgzBRxXFy5uph6Ue6dxyszaA==\n"
                        "-----END PRIVATE KEY-----"
                        )

public_key = "-----BEGIN PUBLIC KEY-----\n" \
             "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzGt41/+kSOTlO1sJvLIN\n" \
             "6RAFaOn6GiCNX/Ju0oVT4VMDHfuQMI5t9+ZgBxFmUhtY5/eykQfYJVGac/cy5xyk\n" \
             "F/1xpMzltK7pfo7XZpfHjkHLPUOeaHW0zE+g2vopQOARKE5LSguCBUhdtfFuiheR\n" \
             "IP0EU+MtEQDhlfiqYLAJkAvZHluCH9q6hawn0t/G873jlzsrXBqIgKboXqyz1lRE\n" \
             "SvMyqX04Xwaq1CgAZjHXBVWvbuOriCR0P2n13/nkCgBgLd/ORwVilb4GQDXkkCSg\n" \
             "uOVcRU3s/KG/OVJTonHVlLvDzBA5GLrpZMpzC4EfzXBM98s4Vj6IOAIQeY84Sppj\n" \
             "qwIDAQAB\n" \
             "-----END PUBLIC KEY-----"

AR_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy8xF9661acn+iS+QS+9Y\n3HvTfUVcismzbuvxHgHA7YeoOUFxyj3lkaTnXm7hzQe4wDEDgwpJSGAzxIIYSUXe\n8EsWLorg5O0tRexx5SP3+kj1i83DATBJCXP7k+bAF4u2FVJphC1m2BfLxelGLjzx\nVAS/v6+EwvYaT1AI9FFqW/a2o92IsVPOh9oM9eds3lBOAbH/8XrmVIeHofw+XbTH\n1/7MLD6IE2+HbEeY0F96nioXArdQWXcjUQsTch+p0p9eqh23Ak4ef5oGcZhNd4yp\nY8M6ppvIMiXkgWSPJevCJjhxRJRmndY+ajYGx7CLePx7wNvxXWtkng3yh+7WiZ/Y\nqwIDAQAB\n-----END PUBLIC KEY-----"

account_id = "fb2921de-592a-49ba-be5e-94044430bc96"
certification_version_id = "edd5d6b7-45bb-4471-898e-ff9c2a7bf56f"


verifying_response = '{"accountId":"fb2921de-592a-49ba-be5e-94044430bc96"}'
onboarding_response = '{"deviceAlternateId":"e2b512f3-9930-4461-b35f-2cdcc7f017fd","capabilityAlternateId":"523e4623-68d2-43d4-a0cc-e2ada2f68b5e","sensorAlternateId":"185cd97b-ed0b-4e75-a6e2-6be1cdd38a06","connectionCriteria":{"gatewayId":"3","measures":"https://dke-qa.eu10.cp.iot.sap/iot/gateway/rest/measures/e2b512f3-9930-4461-b35f-2cdcc7f017fd","commands":"https://dke-qa.eu10.cp.iot.sap/iot/gateway/rest/commands/e2b512f3-9930-4461-b35f-2cdcc7f017fd"},"authentication":{"type":"PEM","secret":"VXHfXV7g#3COYT1Q5YkTxrRXo1IjdN8xSZ3O","certificate":"-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE6zAdBgoqhkiG9w0BDAEDMA8ECHlX0q4qf0tSAgMCAAAEggTI4XIOXehAN02J\nwUrHPe2BCGEqXvyA2QzWMBkqYRm7dCmhL/ay1JzJkkDf2afS/1FE0Sl3So1AMKBe\nhpqZUpaz5g7tN1ktl9BReXC+pptJPpy3XSpZ/8Bg3Jje4eYn2aCWMSNbnw0SO9Sf\nZnUZrNwQH9GSR35fGHYPaYHmAIM9axaUSn6/LfsrifdORY38r9EKvrcuIYFJ18ai\ngHoCAboaPLY52m/UkaM0WNnpTrHm/72G8978jpZKYZmbmp7/qdB7+aQ+WZWs4u/V\nCR6vzgkyWaFzQK5GMKCMBgHteq5900FY9Iz/ZBS/gyoHoVdMsRKRBSXfNebdvADC\nkksZBfaYqMI58CFEuVODi7gD+YKcu7/5BjX8DJ72eDFaYa1ZIC+na24gel8x85UF\n+TwFSQ4NgHmqcUkZJOyRtcnMREP79ZkdGXi4l6eZk4hG9KhfM66HgcvIzGT6e1SF\nJrKcLTVYUdYSyhLZmk7DflgI5VoCKX1/P1O0iiyWqsbqhjfsnfTpaCaveMb+c/2z\nSaw3tc5G6th/QdN72wZTM1Vqb4562JEpxvkxY4i2PW1Ky9HNY0M+jy0DL/KhfnM9\nm8abxdgILTu3WcxnfH7f8uiK2R9zgnIf+CCDtGGWftOGgV5MY4t0XLAsGSadNdqH\nrpTguI4XMcQET0ZEE7fTbkvJ2+QVWz3vD8w4/ryZx12ZzQCoewd5nPQD/JgLoo2R\n8Pdp2TQDYrn0PYZHus1GnPL7kAs34gl1zFNxFF8nYSSP0hITc2zWm8XuLyMc8fgs\nymXZPdTz9LQZPqs5t+P0gL04xegaXiYWWAhZFkMx9/0+zeoNK+w28cTsLRC4oQcJ\nkaq69f7gHIg3ar75Zzzc1xUEgz50oJI2BCDVLllHzoAWFjl5t/9hGcBirP3QOKwg\nCKfHKnbLkSS+2omhp3zBecX7moDS6+RcMMIUvMbHHLx8l4uv/cDtWIh++I21hzQu\ntSaIK6gglGE0OZJN3tPmy3CdHqbapBWvfCMGD2J2xISJCoSwmR58fni4pyniTydt\nJH040YpDUuUxIDlVTFAsmMRm5vh2KkE4DVr1UqA+JJgHRuQiuVbprm/QU2bumTG+\n4vhOKcaSgbQW3++NtvfVSymz5/IJXOMQIzprokvC+6GwiRUBIov7angWwUB9X5iC\nN0rfJ5MbNkabXsFRQpbXYV7z/P+t/9A8A5LBr+DiPLib9i3WI4sHV5aLZapJ3R4u\neBCVB+VIGbcTM19t51h4ohZhY2Q9CYXVnle7ol0Nz/mUiX0Az9oF6GQCngMFdqMh\nftl2XdCq43AZA7hHP+wqKkjOo7i5Lr0IRWw5F7IexV8mHDwx560DJkp0bZM9+UxA\nu1JcTLDJR+a/aOsx5CDSWig+W3XNCQfC4kVhNUlWZ1yQ8Heh+NB3kD+Krvby40DL\nzNOe6VSkFCjKn2st1yJkdcdhLs8mPE1DEk7WRFS+AMaIgXIGpdoBIlUwHpwP7djd\n8gC9e3kFTAazudZkTCi8QnhAeH1coxVhB6+WbzVnFzJDZuy65DiVDSmOjlHmxF7A\nZc5LCo1vmtER3d08bjuz+33dCGS2yKg2Q7Nd3rymUlGzPEx+dPFmvXaDWNXghdbj\nc9PfhpiX5tt83tHe7E2C\n-----END ENCRYPTED PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\nMIIEaTCCA1GgAwIBAgIQAPktOgtD/4tlEAEHAL6qbTANBgkqhkiG9w0BAQsFADBW\nMQswCQYDVQQGEwJERTEjMCEGA1UEChMaU0FQIElvVCBUcnVzdCBDb21tdW5pdHkg\nSUkxIjAgBgNVBAMTGVNBUCBJbnRlcm5ldCBvZiBUaGluZ3MgQ0EwHhcNMjExMDI1\nMTk0MzE1WhcNMjIxMDI1MTk0MzE1WjCBtTELMAkGA1UEBhMCREUxHDAaBgNVBAoT\nE1NBUCBUcnVzdCBDb21tdW5pdHkxFTATBgNVBAsTDElvVCBTZXJ2aWNlczFxMG8G\nA1UEAxRoZGV2aWNlQWx0ZXJuYXRlSWQ6ZTJiNTEyZjMtOTkzMC00NDYxLWIzNWYt\nMmNkY2M3ZjAxN2ZkfGdhdGV3YXlJZDozfHRlbmFudElkOjExMTY5MDM0OTB8aW5z\ndGFuY2VJZDpka2UtcWEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCY\nRAKTeVe2Eo4EtV1QJi1m3gZDpAAXYYhGo8905yw4XZD9M2fCyMbUVcoAm/5lGN+W\nsMk/GsfNeBRmd80SLv6/Z7342tVryhslkGL0TVw2MHMw+1cEAPsH6EthrvH6poTs\ngGDtUB4ad2BOvBwveTPpHwdWxyDUvb74mXwXZ9XgIo/VJKSEr6DlO+zv52BUXRh9\nS70m4dgM0aTM/iRYITrPPXHZfY91M9lsypp64m1dHzDXiQaWvFqaiyIOw/IO2V+O\nMmz3U1Q6L/8ai4WNeTTX69hprOPDTCG5WLdnDviK9hx1w6tOyRdKun7LpklZ14Rv\nApZXATxFwxrNQm2iiFbfAgMBAAGjgdIwgc8wSAYDVR0fBEEwPzA9oDugOYY3aHR0\ncHM6Ly90Y3MubXlzYXAuY29tL2NybC9UcnVzdENvbW11bml0eUlJL1NBUElvVENB\nLmNybDAMBgNVHRMBAf8EAjAAMCUGA1UdEgQeMByGGmh0dHA6Ly9zZXJ2aWNlLnNh\ncC5jb20vVENTMA4GA1UdDwEB/wQEAwIGwDAdBgNVHQ4EFgQUDG1OiFv4Ohku4sG+\n6vC9+x3nCGQwHwYDVR0jBBgwFoAUlbez9Vje1bSzWEbg8qbJeE69LXUwDQYJKoZI\nhvcNAQELBQADggEBADgzaWG5+ch1iQ6tHOHO8/sVBpQJ0kEnHCxDeJ1WRL6Qas/n\nMZPMwzmllsUhQv93fVElGosy2sMjCanCLnCh8qwb85vq7exEZBccbmUo6Epqz9XO\n/NJ4Fr1OWLtE9svRM5s0QEB6B9oQ1OjZtdjeGI9/uQSJgmzYKdI/HAFkTTugokRU\nkyr+rM6Rv9KCNbkzoNTRS6xDNs64FxEw53FBYitmtnsgXAdWPjHpkoZFIntstuFr\nVwpdxeH1TZmdvwhtImibcqGHgUqa7r1lySbK+sEdFzQcf7Ea1dRJR3r1ZfG1/ALn\nRInsXoCBNxyllk6ExpQWiczLiOY5jXnQulX51+k=\n-----END CERTIFICATE-----\n"}}'


message_result = b'[{"sensorAlternateId":"185cd97b-ed0b-4e75-a6e2-6be1cdd38a06","capabilityAlternateId":"bbe9f361-b551-48d9-9fca-1b4dc768287c","command":{"message":"XwjIARAKGiQ5NWUzNWE0Zi1jNWM4LTQ1NDEtODE4OS03NmJlMzM0OTc0NDUiJDUzNzYyM2ZjLWY2NmYtNDc5Yi1hMmJhLWVjZjNlNWM3ZjhlMCoMCNTV5YsGEICI8LIDzQIKygIKTnR5cGVzLmFncmlyb3V0ZXIuY29tL2Fncmlyb3V0ZXIucmVzcG9uc2UucGF5bG9hZC5hY2NvdW50Lkxpc3RFbmRwb2ludHNSZXNwb25zZRL3AQp4CiRkNzA0YTQ0My05OWY3LTQ3YjQtYmU1NS1lMmZhMDk2ODllYmUSJFB5dGhvblNES19kZXYgLSAyMDIxLTEwLTI1LCAxMDo1MToxOBoLYXBwbGljYXRpb24iBmFjdGl2ZTIVdXJuOm15YXBwOnNucjAwMDAzMjM0CnsKJDE4NWNkOTdiLWVkMGItNGU3NS1hNmUyLTZiZTFjZGQzOGEwNhIkUHl0aG9uU0RLX2RldiAtIDIwMjEtMTAtMjEsIDIxOjQxOjI0GgthcHBsaWNhdGlvbiIGYWN0aXZlMhh1cm46bXlhcHA6c25yMDAwMDMyMzRzZGY="}}]'



def test_onboarding():
    from agrirouter.onboarding.enums import GateWays
    import agrirouter as ar
    auth_params = ar.AuthUrlParameter(application_id=application_id, response_type="onboard")
    auth_client = ar.Authorization("QA", public_key=public_key, private_key=private_key)
    auth_url = auth_client.get_auth_request_url(auth_params)

    print(auth_url)

    auth_result_url = input("Entrer url: ")  # the url the user was redirected after his authorization.

    auth_response = auth_client.extract_auth_response(auth_result_url)
    auth_client.verify_auth_response(auth_response)
    auth_response.is_successful
    auth_response.is_valid
    auth_data = auth_response.get_auth_result()

    id_ = "urn:myapp:snr00003234sdf"
    certification_version_id = "edd5d6b7-45bb-4471-898e-ff9c2a7bf56f"
    time_zone = "+03:00"
    onboarding_client = ar.SoftwareOnboarding("QA", public_key=public_key, private_key=private_key)
    onboarding_parameters = ar.SoftwareOnboardingParameter(id_=id_, application_id=application_id,
                                                           certification_version_id=certification_version_id,
                                                           gateway_id=GateWays.MQTT.value,
                                                           time_zone=time_zone,
                                                           reg_code=auth_data.decoded_token.regcode,
                                                           utc_timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z")
    onboarding_verifying_response = onboarding_client.verify(onboarding_parameters)
    onboarding_verifying_response.status_code
    onboarding_verifying_response.text
    print(onboarding_verifying_response.text)
    onboarding_response = onboarding_client.onboard(onboarding_parameters)
    print(onboarding_response.text)

    return onboarding_response


def test_capability_service_http(onboarding_response):
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
    return messaging_result


def test_list_endpoint_service_http(onboarding_response):
    messaging_service = HttpMessagingService()
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


def foo(client, userdata, message):
    print(client, userdata, message)
    return client, userdata, message


def test_list_endpoint_service_mqtt(onboarding_response):
    messaging_service = MqttMessagingService(
        on_message_callback=foo,
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


def test_valid_subscription_service_http(onboarding_response):
    messaging_service = HttpMessagingService()
    subscription_service = SubscriptionService(messaging_service)
    items = []
    for tmt in [CapabilityType.DOC_PDF.value, CapabilityType.ISO_11783_TASKDATA_ZIP.value]:
        subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=tmt)
        items.append(subscription_item)
    subscription_parameters = SubscriptionParameters(
        subscription_items=items,
        onboarding_response=onboarding_response,
        application_message_id=new_uuid(),
        application_message_seq_no=1,
    )
    messaging_result = subscription_service.send(subscription_parameters)
    return messaging_result


def test_query_header_message_http(onboarding_response):
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


def get_outbox(onboarding_response):
    outbox_service = OutboxService()
    outbox_response = outbox_service.fetch(onboarding_response)
    # assert 200 == outbox_response.status_code

    messages = outbox_response.messages
    # assert len(messages) == 1
    # assert messages[0].command.message

    decoded_message = decode_response(outbox_response.messages[0].command.message)
    # assert 204 == decoded_message.response_envelope.response_code

    decoded_details = decode_details(decoded_message.response_payload.details)
    # assert decoded_details

    # query_metrics = decoded_details.query_metrics
    # assert 0 == query_metrics.total_messages_in_query

    return messages, decoded_message, decoded_details


def test_outbox_service_http(onboarding_response):
    outbox_service = OutboxService()
    result = outbox_service.fetch(onboarding_response)
    return result


def test_revoke():
    params = RevokingParameter(
        application_id=application_id,
        account_id=account_id,
        endpoint_ids=[
            "849ff5b9-6b3a-418e-9394-931e19acb8ec",
            "b2157913-013f-486c-bf25-a591ffca451b"
        ],
        utc_timestamp=now_as_utc_str(),
        time_zone="+03:00",
        content_type=ContentTypes.APPLICATION_JSON.value
    )
    service = Revoking("QA", public_key=public_key, private_key=private_key)
    return service.revoke(params)


def test():
    onboarding_response = test_onboarding()
    # print(test_list_endpoint_service_http(onboarding_response).get_messages_ids())
    # print(test_valid_subscription_service_http(onboarding_response).get_messages_ids())
    # print(test_capability_service_http(onboarding_response).get_messages_ids())
    # print(test_list_endpoint_service_http(onboarding_response).get_messages_ids())
    messaging_result = test_list_endpoint_service_mqtt(onboarding_response)
    return messaging_result


if __name__ == "__main__":
    test()
