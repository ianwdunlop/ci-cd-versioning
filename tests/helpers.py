def fake_response(code: int, body: dict = None):
    def side_effect(*args, **kwargs):
        class Resp:
            def __init__(self, c: int, b: dict = None):
                self.status_code = c
                self.body = b

            def json(self):
                return self.body

        return Resp(code, body)
    return side_effect
