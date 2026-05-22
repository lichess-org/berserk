"""Unit tests for check-endpoints.py (dev tool). Not run by make test.

Run manually: uv run pytest dev_tests/test_check_endpoints.py -v
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

# Load check-endpoints.py (hyphen in name) as a module
_ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "check_endpoints", _ROOT / "check-endpoints.py"
)
assert _SPEC is not None and _SPEC.loader is not None
check_endpoints = importlib.util.module_from_spec(_SPEC)
sys.modules["check_endpoints"] = check_endpoints
_SPEC.loader.exec_module(check_endpoints)


class TestNormalizePathTemplate:
    def test_leading_slash_added(self):
        assert check_endpoints.normalize_path_template("api/games") == "/api/games"

    def test_trailing_slash_removed(self):
        assert check_endpoints.normalize_path_template("/api/games/") == "/api/games"

    def test_placeholder_collapsed(self):
        assert (
            check_endpoints.normalize_path_template("/api/game/{id}") == "/api/game/{}"
        )
        assert (
            check_endpoints.normalize_path_template("/api/{gameId}/claim")
            == "/api/{}/claim"
        )

    def test_query_stripped(self):
        assert check_endpoints.normalize_path_template("/api?page=1") == "/api"
        assert check_endpoints.normalize_path_template("/api?page=1&foo=bar") == "/api"

    def test_unchanged_when_already_normalized(self):
        assert check_endpoints.normalize_path_template("/api/games") == "/api/games"


class TestQueryParamKeysFromPath:
    def test_no_query_returns_empty(self):
        assert check_endpoints.query_param_keys_from_path("/api") == set()
        assert check_endpoints.query_param_keys_from_path(None) == set()
        assert check_endpoints.query_param_keys_from_path("") == set()

    def test_single_param(self):
        assert check_endpoints.query_param_keys_from_path("/api?page=1") == {"page"}

    def test_multiple_params(self):
        assert check_endpoints.query_param_keys_from_path("/api?a=1&b=2") == {"a", "b"}


class TestSpecQueryParams:
    def test_empty_path_item(self):
        assert check_endpoints.spec_query_params({}, "get") == set()

    def test_operation_level_query_params(self):
        path_item = {
            "get": {
                "parameters": [
                    {"name": "page", "in": "query"},
                    {"name": "Accept", "in": "header"},
                ]
            }
        }
        assert check_endpoints.spec_query_params(path_item, "get") == {"page"}

    def test_path_level_and_operation_merged(self):
        path_item = {
            "parameters": [{"name": "common", "in": "query"}],
            "get": {"parameters": [{"name": "page", "in": "query"}]},
        }
        assert check_endpoints.spec_query_params(path_item, "get") == {"common", "page"}


class TestSpecPathOperations:
    def test_yields_path_and_operation(self):
        spec = {
            "paths": {
                "/api/games": {"get": {}},
                "/api/user": {"get": {}, "post": {}},
            }
        }
        out = list(check_endpoints.spec_path_operations(spec))
        assert ("/api/games", spec["paths"]["/api/games"], "get") in out
        assert ("/api/user", spec["paths"]["/api/user"], "get") in out
        assert ("/api/user", spec["paths"]["/api/user"], "post") in out
        assert len(out) == 3


class TestFalsePositives:
    def test_expected_paths_excluded(self):
        assert "/oauth" in check_endpoints.FALSE_POSITIVES
        assert "/standard" in check_endpoints.FALSE_POSITIVES
        assert "/atomic" in check_endpoints.FALSE_POSITIVES
        assert "/antichess" in check_endpoints.FALSE_POSITIVES


def _run_script(
    *args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run check-endpoints.py; cwd defaults to repo root."""
    cmd = [sys.executable, str(_ROOT / "check-endpoints.py"), *args]
    return subprocess.run(
        cmd,
        cwd=cwd or _ROOT,
        capture_output=True,
        text=True,
    )


_FIXTURES = _ROOT / "dev_tests" / "fixtures"
_FAKE_CLIENTS = _FIXTURES / "fake_clients"


class TestExitCode:
    """Script exit code: 0 on success, non-zero on error."""

    def test_no_args_exits_non_zero(self):
        result = _run_script()
        assert result.returncode != 0
        assert "Usage" in result.stderr or "Spec file not found" in result.stderr

    def test_nonexistent_spec_exits_non_zero(self):
        result = _run_script("nonexistent.yaml")
        assert result.returncode != 0
        assert "not found" in result.stderr or "Spec file" in result.stderr

    def test_valid_spec_exits_zero(self):
        spec_path = _ROOT / "dev_tests" / "fixtures" / "minimal_spec.yaml"
        result = _run_script("--json", str(spec_path))
        assert result.returncode == 0, result.stderr

    def test_clients_dir_nonexistent_exits_non_zero(self):
        spec_path = _FIXTURES / "minimal_spec.yaml"
        result = _run_script("--json", "--clients-dir", "/nonexistent", str(spec_path))
        assert result.returncode != 0
        assert "not found" in result.stderr or "Clients dir" in result.stderr


class TestJsonOutput:
    """With --json, stdout is valid JSON with expected keys and types."""

    def test_json_has_required_keys(self):
        spec_path = _ROOT / "dev_tests" / "fixtures" / "minimal_spec.yaml"
        result = _run_script("--json", str(spec_path))
        result.check_returncode()
        data = json.loads(result.stdout)
        assert "missing_endpoints" in data
        assert "missing_params" in data

    def test_missing_endpoints_and_params_are_lists(self):
        spec_path = _ROOT / "dev_tests" / "fixtures" / "minimal_spec.yaml"
        result = _run_script("--json", str(spec_path))
        result.check_returncode()
        data = json.loads(result.stdout)
        assert isinstance(data["missing_endpoints"], list)
        assert isinstance(data["missing_params"], list)

    def test_missing_endpoint_item_has_path_and_operation(self):
        """When there are missing endpoints, each item has path and operation."""
        spec_path = _ROOT / "dev_tests" / "fixtures" / "minimal_spec.yaml"
        result = _run_script("--json", str(spec_path))
        result.check_returncode()
        data = json.loads(result.stdout)
        # Minimal spec has /api/minimal-test get which we don't implement
        assert len(data["missing_endpoints"]) >= 1
        item = data["missing_endpoints"][0]
        assert "path" in item
        assert "operation" in item

    def test_missing_params_item_has_path_operation_params_and_method(self):
        """Fixture client implements one param; spec adds another → one missing_params entry with correct shape."""
        spec_path = _FIXTURES / "spec_with_extra_param.yaml"
        result = _run_script(
            "--json",
            "--clients-dir",
            str(_FAKE_CLIENTS),
            str(spec_path),
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert len(data["missing_params"]) == 1, data
        item = data["missing_params"][0]
        assert item["path"] == "/api/dev-tests/fixture"
        assert item["operation"] == "GET"
        assert "params" in item
        assert "method" in item
        assert isinstance(item["params"], list)
        assert item["params"] == ["b"]

    def test_missing_endpoint_reported_when_not_implemented(self):
        """Fixture implements one path; spec has two. Unimplemented path appears in missing_endpoints."""
        spec_path = _FIXTURES / "spec_one_missing_endpoint.yaml"
        result = _run_script(
            "--json",
            "--clients-dir",
            str(_FAKE_CLIENTS),
            str(spec_path),
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert len(data["missing_endpoints"]) == 1, data
        assert data["missing_endpoints"][0]["path"] == "/api/dev-tests/other"
        assert data["missing_endpoints"][0]["operation"] == "GET"

    def test_no_missing_when_spec_and_client_match(self):
        """Fixture and spec match exactly → empty missing_endpoints and missing_params."""
        spec_path = _FIXTURES / "spec_exact_match.yaml"
        result = _run_script(
            "--json",
            "--clients-dir",
            str(_FAKE_CLIENTS),
            str(spec_path),
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert data["missing_endpoints"] == [], data
        assert data["missing_params"] == [], data

    def test_false_positive_not_reported_as_missing(self):
        """Spec with only /oauth (in FALSE_POSITIVES) → missing_endpoints is empty."""
        spec_path = _FIXTURES / "spec_false_positive_only.yaml"
        result = _run_script("--json", str(spec_path))
        result.check_returncode()
        data = json.loads(result.stdout)
        assert data["missing_endpoints"] == [], data


class TestDiscoveryCodePaths:
    """Integration tests: script discovers endpoints for real code patterns (f-string, request(), path=, params var)."""

    def test_fstring_path_discovered(self):
        """Visitor resolves JoinedStr path (f\"/api/.../{id}\") → normalized /api/.../{}."""
        spec_path = _FIXTURES / "spec_fstring.yaml"
        result = _run_script(
            "--json", "--clients-dir", str(_FAKE_CLIENTS), str(spec_path)
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert data["missing_endpoints"] == [], data

    def test_request_method_path_discovered(self):
        """Visitor finds self._r.request(method=\"GET\", path=path)."""
        spec_path = _FIXTURES / "spec_request_method.yaml"
        result = _run_script(
            "--json", "--clients-dir", str(_FAKE_CLIENTS), str(spec_path)
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert data["missing_endpoints"] == [], data

    def test_path_keyword_discovered(self):
        """Visitor finds path passed as keyword: self._r.get(path=path)."""
        spec_path = _FIXTURES / "spec_path_keyword.yaml"
        result = _run_script(
            "--json", "--clients-dir", str(_FAKE_CLIENTS), str(spec_path)
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert data["missing_endpoints"] == [], data

    def test_params_from_variable_discovered(self):
        """Visitor resolves params=params when params was assigned a dict earlier → missing param 'r' reported."""
        spec_path = _FIXTURES / "spec_params_variable.yaml"
        result = _run_script(
            "--json", "--clients-dir", str(_FAKE_CLIENTS), str(spec_path)
        )
        result.check_returncode()
        data = json.loads(result.stdout)
        assert data["missing_endpoints"] == [], data
        assert len(data["missing_params"]) == 1, data
        item = data["missing_params"][0]
        assert item["path"] == "/api/dev-tests/params-var"
        assert item["params"] == ["r"]


class TestHumanOutput:
    """Without --json, human-readable output."""

    def test_nothing_missing_printed_when_all_match(self):
        """Exact match → stdout contains 'Nothing missing'."""
        spec_path = _FIXTURES / "spec_exact_match.yaml"
        result = _run_script("--clients-dir", str(_FAKE_CLIENTS), str(spec_path))
        result.check_returncode()
        assert "Nothing missing" in result.stdout
