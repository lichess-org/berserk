# Fixture for integration test: visitor discovers self._r.request(method=..., path=...).


class RequestMethodClient:
    def get_via_request(self):
        path = "/api/dev-tests/request-method"
        return self._r.request(method="GET", path=path)
