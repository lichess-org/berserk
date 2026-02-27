"""Test utility shim.

The repository contains two separate test suites:
- tests/clients (unit-ish, VCR-based)
- integration/tests

Both historically imported helpers from a top-level `utils` module.
When running `pytest` from the repository root, Python may resolve `utils`
from `integration/tests/utils.py` instead of `tests/clients/utils.py`,
which breaks client test collection.

This shim re-exports the helpers used by the client tests.
"""

from tests.clients.utils import skip_if_older_3_dot_10, validate

__all__ = ["skip_if_older_3_dot_10", "validate"]
