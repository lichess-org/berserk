# Berserk: Python Lichess API Client

Berserk is a Python client library for the Lichess chess API. It handles JSON/PGN formats, supports token authentication and OAuth2, and provides comprehensive coverage of the Lichess API endpoints.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

**Bootstrap and setup the development environment:**
- Install Poetry: `pip3 install poetry`
- Install all dependencies: `poetry install --with dev` OR `make setup`  
  - Takes 2-3 minutes initially but subsequent operations are very fast
- Verify installation: `poetry run python3 -c "import berserk; print('✓ Berserk installed:', berserk.__version__)"`

**Testing the library (ALWAYS run after making changes):**
- Run test suite: `poetry run pytest tests` OR `make test`
  - Takes ~0.4 seconds (47 tests), ~2 seconds total with overhead
- Run type checking: `poetry run pyright berserk` OR `make typecheck`
  - Takes ~5 seconds (includes npm install for pyright)  
- Check code formatting: `poetry run black berserk tests check-endpoints.py --check` OR `make format --check`
  - Takes ~1 second

**Code quality and formatting:**
- Format code: `poetry run black berserk tests check-endpoints.py` OR `make format`
  - Takes ~1 second
- Also format docstrings: `poetry run docformatter --in-place --black berserk/*.py`

**Documentation:**
- Build documentation: `poetry run sphinx-build -b html docs _build -EW --keep-going` OR `make docs`
  - Takes ~5 seconds
- Serve docs locally: `make servedocs` (serves on http://localhost:8000)

**Optional setup:**
- Install pre-commit hook: `cp hooks/pre-commit .git/hooks/pre-commit`
- Check missing API endpoints: `python3 check-endpoints.py /path/to/lichess-api.yaml` (requires `pip3 install pyyaml`)

## Validation Scenarios

**ALWAYS validate your changes by running these scenarios after making any code modifications:**

1. **Basic Library Import Test:**
```python
import berserk
client = berserk.Client()
print("✓ Client created:", [attr for attr in dir(client) if not attr.startswith('_')][:5])
```

2. **Authentication Test:**
```python
import berserk
session = berserk.TokenSession('test_token')
client = berserk.Client(session=session)
print("✓ Authenticated client created")
```

3. **Format Handler Test:**
```python
import berserk.formats as formats
print("✓ Available formats:", [attr for attr in dir(formats) if attr.isupper()])
```

4. **Complete Validation Sequence:**
- `make test` - All tests must pass
- `make typecheck` - Type checking must pass with 0 errors
- `make format --check` - Code must be properly formatted
- Run the basic import tests above manually

## Common Tasks

**Repository structure:**
```
/berserk/           # Main library code
├── clients/        # API client modules (account, games, tournaments, etc.)
├── __init__.py     # Library entry point
├── session.py      # Authentication handling
├── formats.py      # JSON/PGN format handlers
└── utils.py        # Utility functions

/tests/             # Unit tests (47 tests, very fast)
├── clients/        # Client-specific tests
└── test_*.py       # Core functionality tests

/integration/       # Integration tests (requires Docker + local Lichess)
/docs/              # Sphinx documentation
/.github/workflows/ # CI: test.yml, typing.yml, format.yml, docs.yml, integration_test.yml
```

**Key files:**
- `pyproject.toml` - Poetry project configuration, dependencies, Python 3.8+ requirement
- `Makefile` - Convenient commands for all development tasks
- `CONTRIBUTING.rst` - Detailed contribution guidelines with test writing examples
- `check-endpoints.py` - Script to compare implemented vs. available API endpoints

**Python compatibility:**
- Requires Python 3.8+
- Tested on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Uses Poetry for dependency management (NOT pip directly)

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

## Integration Testing

**Docker-based integration tests:**
- Requires Docker and `ghcr.io/lichess-org/lila-docker:main` image
- Use test tokens: `lip_bobby`, `lip_zerogames` 
- Run with: `./integration/local.sh` or manually:
  - `docker run --name bdit_lila --network bdit_network -d ghcr.io/lichess-org/lila-docker:main`
  - `./integration/run-tests.sh`

**Integration tests verify:**
- Account operations (get, email, preferences, kid mode, bot upgrade)
- Real API interactions against local Lichess instance
- Authentication token handling

## CI/CD Pipeline

**GitHub Actions workflows:**
- `test.yml` - Runs tests on Python 3.8-3.12 across Ubuntu/macOS/Windows
- `typing.yml` - Type checking with pyright on all Python versions  
- `format.yml` - Code formatting verification with black
- `docs.yml` - Documentation building and deployment
- `integration_test.yml` - Docker-based integration tests
- `codeql.yml` - Security analysis

**Pre-release checklist (for maintainers):**
- Update `CHANGELOG.rst`
- Bump version in `pyproject.toml`
- Run `make publish` (requires PyPI credentials)
- Tag release: `git tag v1.2.3 && git push --tags`

## Notes

- This is a **library**, not an application - there's no server to run or UI to interact with
- All development commands are very fast (under 6 seconds each after initial setup)
- No build step required - it's pure Python
- Focus validation on import patterns and API client functionality
- The library works with or without authentication (some endpoints are public)
- Network access is required for real API calls during manual testing
- Integration tests provide the most comprehensive validation but require Docker setup