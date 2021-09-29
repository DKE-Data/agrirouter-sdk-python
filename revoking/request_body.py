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
            "account_id": account_id,
            "endpoint_ids": endpoint_ids,
            "UTCTimestamp": utc_timestamp,
            "timeZone": time_zone,
        }

    def json(self, new_lines: bool = True) -> str:
        result = json.dumps(self.get_parameters(), indent="")
        if not new_lines:
            return result.replace("\n", "")
        return result
