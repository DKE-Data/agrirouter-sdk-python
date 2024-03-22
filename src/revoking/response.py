from requests import Response


class RevokingResponse:
    """
    Response from revoking request
    """

    def __init__(self, http_response: Response):
        self.response: Response = http_response

    @property
    def data(self):
        return self.response.json()

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def text(self):
        return self.response.text
