
class BadAuthResponse(Exception):
    def __init__(self, message=None):
        if not message:
            message = "Bad Response. Response could is not verified."
        self.message = message
