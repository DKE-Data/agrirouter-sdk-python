class HttpClient:

    headers = {"Content-Type": "application/json"}

    def __init__(self,
                 on_message_callback: callable,
                 timeout=20
                 ):
        self.on_message_callback = on_message_callback
        self.timeout = timeout

    def publish(self):
        pass

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    def _start_loop(self):
        pass
