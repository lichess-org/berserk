# Fixture for integration test: visitor discovers f-string path (JoinedStr).
# Script normalizes to /api/dev-tests/fstring/{}.


class FstringClient:
    def get_with_fstring(self, id):
        path = f"/api/dev-tests/fstring/{id}"
        return self._r.get(path)
