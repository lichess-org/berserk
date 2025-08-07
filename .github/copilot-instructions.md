# Berserk: Python Lichess API Client

Berserk is a Python client library for the Lichess chess API. It handles JSON/PGN formats, supports token authentication and OAuth2, and provides comprehensive coverage of the Lichess API endpoints.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Code Standards

### Required Before Each Commit
- Run `make format` before committing any changes to ensure proper code formatting

## Development Setup & Workflow

**For complete development setup and contribution guidelines, see [CONTRIBUTING.rst](../CONTRIBUTING.rst).**

### Validation Scenarios

**For complete testing guidelines, see [CONTRIBUTING.rst](../CONTRIBUTING.rst) and [pull_request_template.md](pull_request_template.md)**

## Repository Overview

**Repository structure:**
```
/berserk/           # Main library code
├── clients/        # API client modules (account, games, tournaments, etc.)
├── __init__.py     # Library entry point
├── session.py      # Authentication handling
├── formats.py      # JSON/PGN format handlers
└── utils.py        # Utility functions

/tests/             # Unit tests (very fast)
├── clients/        # Client-specific tests
└── test_*.py       # Core functionality tests

/integration/       # Integration tests (requires Docker + local Lichess)
/docs/              # Sphinx documentation
/.github/workflows/ # CI: test.yml, typing.yml, format.yml, docs.yml, integration_test.yml
```

**Key files:**
- `pyproject.toml` - project configuration, dependencies
- `Makefile` - Convenient commands for all development tasks
- `CONTRIBUTING.rst` - **Complete contribution guidelines and setup instructions**
- `check-endpoints.py` - Script to compare implemented vs. available API endpoints

**API Client Modules:**
The client provides these main modules:
- `client.account` - Account management
- `client.games` - Game data and streaming  
- `client.tournaments` - Tournament operations
- `client.users` - User data and statistics
- `client.board` - Board API for playing
- `client.bots` - Bot API
- `client.challenges` - Challenge management
- `client.studies` - Study operations
- And many more (see README.rst for complete list)