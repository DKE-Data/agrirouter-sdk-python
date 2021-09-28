from constants.media_types import ContentTypes


class RevokingParameter:

    def __init__(self,
                 application_id,
                 account_id,
                 endpoint_ids,
                 utc_timestamp,
                 timestamp,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):

        self.application_id = application_id
        self.content_type = content_type
        self.account_id = account_id
        self.endpoint_ids = endpoint_ids
        self.utc_timestamp = utc_timestamp
        self.timestamp = timestamp

    def get_header_params(self):
        return {
            "application_id": self.application_id,
            "content_type": self.content_type,
        }

    def get_body_params(self):
        return {
            "account_id": self.account_id,
            "endpoint_ids": self.endpoint_ids,
            "utc_timestamp": self.utc_timestamp,
            "timestamp": self.timestamp,
        }
