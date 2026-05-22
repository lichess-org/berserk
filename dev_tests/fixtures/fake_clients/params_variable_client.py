# Fixture for integration test: visitor discovers params from variable (params_scope).
# Assign params = {"q": q}, then pass params=params. Spec adds "r" so we get one missing param.


class ParamsVariableClient:
    def get_with_params_var(self, q):
        path = "/api/dev-tests/params-var"
        params = {"q": q}
        return self._r.get(path, params=params)
