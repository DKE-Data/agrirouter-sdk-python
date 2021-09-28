class RevokingResponse:
    """
    Response from revoking request
    """

    def __init__(self, http_response):
        self.response = http_response
