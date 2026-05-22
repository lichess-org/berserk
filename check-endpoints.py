#!/usr/bin/env python3
"""Check that client code implements all (path, operation) pairs from the API spec.

Uses AST parsing to find path assignments and _r.get/post/put/patch/delete/request
calls so we match (path, operation) accurately, including when path is passed
as a variable or as a literal/f-string. For implemented endpoints, also checks
that query params passed to the request match the spec.

Exit codes: 0 = success (run completed; check JSON or human output for missing/not);
non-zero = error (bad args, spec not found, exception). With --json, only JSON is
printed to stdout for CI; empty missing_endpoints and missing_params means nothing missing.
Errors always go to stderr.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import traceback
from pathlib import Path

import yaml

EXIT_ERROR = 1

# Paths that appear in spec but are implemented dynamically (e.g. tablebase /{variant})
FALSE_POSITIVES = {"/standard", "/atomic", "/antichess", "/oauth"}

# HTTP methods we care about (OpenAPI operation keys)
OPERATIONS = ("get", "post", "put", "patch", "delete")


def _dict_literal_keys(node: ast.Dict) -> set[str]:
    """Return set of string keys from a dict literal. Non-string keys are skipped."""
    keys: set[str] = set()
    for k in node.keys:
        if k is not None and isinstance(k, ast.Constant) and isinstance(k.value, str):
            keys.add(k.value)
    return keys


def param_keys_from_node(
    node: ast.AST | None, params_scope: dict[str, set[str]]
) -> set[str] | None:
    """Resolve param keys from AST: literal dict, or Name looked up in params_scope. None = unresolved."""
    if node is None:
        return set()
    if isinstance(node, ast.Dict):
        return _dict_literal_keys(node)
    if isinstance(node, ast.Name):
        return params_scope.get(node.id)
    return None


def query_param_keys_from_path(path_template: str | None) -> set[str]:
    """Extract query param names from a path string that may contain ?key=value&... (e.g. f\"...?page={page}\")."""
    if not path_template or "?" not in path_template:
        return set()
    query_part = path_template.split("?", 1)[1].split("#")[0]
    keys: set[str] = set()
    for pair in query_part.split("&"):
        if "=" in pair:
            keys.add(pair.split("=", 1)[0].strip())
        elif pair.strip():
            keys.add(pair.strip())
    return keys


def normalize_path_template(path: str) -> str:
    """Canonical form for matching: leading slash, placeholders as {}, no trailing slash."""
    # Query string is not part of the path for spec matching
    if "?" in path:
        path = path.split("?", 1)[0]
    path = path.strip().rstrip("/")
    if path and not path.startswith("/"):
        path = "/" + path
    # Collapse any {param} to {} so spec and code match regardless of param names
    return re.sub(r"\{[^}/]+\}", "{}", path)


def path_template_from_ast_node(node: ast.AST, scope: dict[str, str]) -> str | None:
    """Resolve a path value from an AST node (Constant, JoinedStr, or Name in scope)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                # Any placeholder; we don't need the variable name for matching
                parts.append("{}")
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.Name):
        return scope.get(node.id)
    return None


class PathOperationVisitor(ast.NodeVisitor):
    """Collect (normalized_path, operation), param keys, and method location from _r.get/post/.../request calls."""

    def __init__(self, source_file: Path | None = None) -> None:
        self.found: set[tuple[str, str]] = set()
        self.implemented_params: dict[tuple[str, str], set[str]] = {}
        self.implemented_method_info: dict[tuple[str, str], tuple[str, str, str]] = {}
        self._scope: dict[str, str] = {}
        self._params_scope: dict[str, set[str]] = {}
        self._source_file = source_file
        self._current_class: str | None = None
        self._current_function: ast.FunctionDef | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        old_class = self._current_class
        self._current_class = node.name
        self.generic_visit(node)
        self._current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        old_scope = self._scope.copy()
        old_params_scope = self._params_scope.copy()
        old_function = self._current_function
        self._current_function = node
        # First pass: collect path assignments and params dict assignments
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        template = path_template_from_ast_node(stmt.value, self._scope)
                        if template is not None:
                            self._scope[target.id] = template
                        if isinstance(stmt.value, ast.Dict):
                            self._params_scope[target.id] = _dict_literal_keys(
                                stmt.value
                            )
        self.generic_visit(node)
        self._scope = old_scope
        self._params_scope = old_params_scope
        self._current_function = old_function

    def _add(
        self,
        path_template: str | None,
        operation: str,
        param_keys: set[str] | None,
    ) -> None:
        if path_template is None:
            return
        normalized = normalize_path_template(path_template)
        if not normalized:
            return
        op = operation.lower()
        key = (normalized, op)
        self.found.add(key)
        # Record first-seen method location for this (path, op)
        if key not in self.implemented_method_info and self._source_file is not None:
            class_name = self._current_class or ""
            method_name = self._current_function.name if self._current_function else ""
            self.implemented_method_info[key] = (
                str(self._source_file),
                class_name,
                method_name,
            )
        # Param keys from params= dict plus any interpolated in path (?key=...)
        keys = set(param_keys) if param_keys else set()
        keys |= query_param_keys_from_path(path_template)
        if keys:
            self.implemented_params.setdefault(key, set()).update(keys)

    def visit_Call(self, node: ast.Call) -> None:
        # Detect self._r.get(...), self._r.post(...), self._r.request(...)
        if not isinstance(node.func, ast.Attribute):
            self.generic_visit(node)
            return
        attr = node.func.attr
        if not isinstance(node.func.value, ast.Attribute):
            self.generic_visit(node)
            return
        if node.func.value.attr != "_r":
            self.generic_visit(node)
            return
        # self._r.<method>(...)
        params_node = None
        for kw in node.keywords:
            if kw.arg == "params":
                params_node = kw.value
                break

        if attr in ("get", "post", "put", "patch", "delete"):
            # First positional is path, or path= keyword
            path_node = None
            for i, arg in enumerate(node.args):
                if i == 0:
                    path_node = arg
                    break
            if path_node is None:
                for kw in node.keywords:
                    if kw.arg == "path":
                        path_node = kw.value
                        break
            if path_node is not None:
                template = path_template_from_ast_node(path_node, self._scope)
                param_keys = param_keys_from_node(params_node, self._params_scope)
                self._add(template, attr, param_keys)
        elif attr == "request":
            # request(method, path, ...) or request(method=..., path=...)
            method_val = None
            path_node = None
            if len(node.args) >= 2:
                method_val = node.args[0]
                path_node = node.args[1]
            for kw in node.keywords:
                if kw.arg == "method":
                    method_val = kw.value
                elif kw.arg == "path":
                    path_node = kw.value
            if path_node is not None and method_val is not None:
                if isinstance(method_val, ast.Constant) and isinstance(
                    method_val.value, str
                ):
                    template = path_template_from_ast_node(path_node, self._scope)
                    param_keys = param_keys_from_node(params_node, self._params_scope)
                    self._add(template, method_val.value.lower(), param_keys)
        self.generic_visit(node)


def discover_implemented_path_operations(
    clients_dir: Path,
) -> tuple[
    set[tuple[str, str]],
    dict[tuple[str, str], set[str]],
    dict[tuple[str, str], tuple[str, str, str]],
]:
    """Parse all client modules; return (implemented (path, op), param keys, method info)."""
    implemented: set[tuple[str, str]] = set()
    implemented_params: dict[tuple[str, str], set[str]] = {}
    implemented_method_info: dict[tuple[str, str], tuple[str, str, str]] = {}
    for py_path in sorted(clients_dir.glob("*.py")):
        try:
            tree = ast.parse(py_path.read_text())
        except SyntaxError:
            continue
        visitor = PathOperationVisitor(source_file=py_path)
        visitor.visit(tree)
        implemented |= visitor.found
        for key, keys in visitor.implemented_params.items():
            implemented_params.setdefault(key, set()).update(keys)
        for key, info in visitor.implemented_method_info.items():
            if key not in implemented_method_info:
                implemented_method_info[key] = info
    return (implemented, implemented_params, implemented_method_info)


def spec_query_params(path_item: dict, op: str) -> set[str]:
    """Return set of query param names for this path + operation (path-level and operation-level merged)."""
    path_params = path_item.get("parameters") or []
    op_obj = path_item.get(op)
    op_params = (op_obj.get("parameters") or []) if isinstance(op_obj, dict) else []
    by_name: dict[str, dict] = {}
    for p in path_params:
        if isinstance(p, dict) and p.get("name"):
            by_name[p["name"]] = p
    for p in op_params:
        if isinstance(p, dict) and p.get("name"):
            by_name[p["name"]] = p
    return {p["name"] for p in by_name.values() if p.get("in") == "query"}


def spec_path_operations(spec: dict):
    """Yield (path_str, path_item, operation) from OpenAPI spec paths."""
    for path_str, path_item in spec.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for op in OPERATIONS:
            if op in path_item:
                yield (path_str, path_item, op)


def main() -> None:
    argv = sys.argv[1:]
    json_output = "--json" in argv
    args = [a for a in argv if a != "--json"]

    clients_dir = Path("berserk/clients")
    if "--clients-dir" in args:
        idx = args.index("--clients-dir")
        if idx + 1 >= len(args):
            print("Usage: --clients-dir requires a path", file=sys.stderr)
            sys.exit(EXIT_ERROR)
        clients_dir = Path(args[idx + 1])
        args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]

    if len(args) != 1:
        spec_path = Path("../api/doc/specs/lichess-api.yaml")
        if not spec_path.is_file():
            print(
                "Usage: check-endpoints.py [--json] [--clients-dir DIR] <path to lichess-api.yaml>",
                file=sys.stderr,
            )
            sys.exit(EXIT_ERROR)
    else:
        spec_path = Path(args[0])
        if not spec_path.is_file():
            print(f"Spec file not found: {spec_path}", file=sys.stderr)
            sys.exit(EXIT_ERROR)

    try:
        with open(spec_path) as f:
            spec = yaml.load(f, Loader=yaml.SafeLoader)
    except OSError as e:
        print(f"Error reading spec: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if not clients_dir.is_dir():
        print(f"Clients dir not found: {clients_dir}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    implemented, implemented_params, implemented_method_info = (
        discover_implemented_path_operations(clients_dir)
    )

    def _format_method(file: str, class_name: str, method_name: str) -> str:
        if class_name and method_name:
            return f"{file}: {class_name}.{method_name}"
        if method_name:
            return f"{file}: {method_name}"
        return file

    missing: list[tuple[str, str]] = []
    for path_str, path_item, op in spec_path_operations(spec):
        path_norm = normalize_path_template(path_str)
        if path_norm in FALSE_POSITIVES:
            continue
        if (path_norm, op) not in implemented:
            # When path has its own servers (e.g. tablebase), show full URL in output
            if servers := path_item.get("servers"):
                if host := servers[0].get("url"):
                    path_str = host + path_str
            missing.append((path_str, op))

    missing_params_list: list[tuple[str, str, set[str], str]] = []
    for path_str, path_item, op in spec_path_operations(spec):
        path_norm = normalize_path_template(path_str)
        if path_norm in FALSE_POSITIVES:
            continue
        if (path_norm, op) not in implemented:
            continue
        spec_params = spec_query_params(path_item, op)
        if not spec_params:
            continue
        implemented_keys = implemented_params.get((path_norm, op))
        if implemented_keys is None:
            continue
        missing_params = spec_params - implemented_keys
        if missing_params:
            if servers := path_item.get("servers"):
                if host := servers[0].get("url"):
                    path_str = host + path_str
            info = implemented_method_info.get((path_norm, op), ("", "", ""))
            method_str = _format_method(info[0], info[1], info[2])
            missing_params_list.append((path_str, op, missing_params, method_str))

    has_missing = bool(missing) or bool(missing_params_list)

    if json_output:
        out = {
            "missing_endpoints": [
                {"path": p, "operation": op.upper()} for p, op in sorted(missing)
            ],
            "missing_params": [
                {
                    "path": p,
                    "operation": op.upper(),
                    "params": sorted(ps),
                    "method": method_str,
                }
                for p, op, ps, method_str in sorted(
                    missing_params_list, key=lambda x: (x[0], x[1])
                )
            ],
        }
        print(json.dumps(out, indent=2))
    else:
        if not has_missing:
            print("Nothing missing")
        else:
            if missing:
                print("\nMissing (path, operation):\n")
                for path, op in sorted(missing):
                    print(f"  {path}  {op.upper()}")
            if missing_params_list:
                print("\nMissing query params (implemented endpoints):\n")
                for path, op, params, method_str in sorted(
                    missing_params_list, key=lambda x: (x[0], x[1])
                ):
                    print(
                        f"  {path}  {op.upper()}  missing params: {sorted(params)}  ({method_str})"
                    )

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(EXIT_ERROR)
