# Only for dev_tests/test_check_endpoints.py. Implements GET /api/dev-tests/fixture
# with param "a"; spec adds "b" so script reports one missing_params entry.
# Script only parses AST; this file is never imported.


class FixtureClient:
    def get_fixture(self, a):
        path = "/api/dev-tests/fixture"
        params = {"a": a}
        return self._r.get(path, params=params)
