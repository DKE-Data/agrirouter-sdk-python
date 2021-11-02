import json


class RevokingBody:
    def __init__(self,
                 account_id,
                 endpoint_ids,
                 utc_timestamp,
                 time_zone):

        self._set_params(
            account_id,
            endpoint_ids,
            utc_timestamp,
            time_zone
        )

    def get_parameters(self) -> dict:
        return self.params

    def _set_params(self,
                    account_id,
                    endpoint_ids,
                    utc_timestamp,
                    time_zone
                    ) -> None:

        self.params = {
            "accountId": account_id,
            "endpointIds": endpoint_ids,
            "UTCTimestamp": utc_timestamp,
            "timeZone": time_zone,
        }

    def json(self) -> str:
        return json.dumps(self.get_parameters(), separators=(',', ':'))
