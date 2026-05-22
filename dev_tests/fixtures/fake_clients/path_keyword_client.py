# Fixture for integration test: visitor discovers path passed as keyword (path=path).


class PathKeywordClient:
    def get_with_path_keyword(self):
        path = "/api/dev-tests/path-keyword"
        return self._r.get(path=path)
