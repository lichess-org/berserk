import time
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--throttle-time",
        type=float,
        default=0.0,
        help="Sleep N seconds after each test (useful when running against real APIs).",
    )


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "match_on": ["method", "scheme", "host", "port", "path", "query", "body"],
        "decode_compressed_response": True,
    }


@pytest.fixture(autouse=True)
def throttle_between_tests(request):
    throttle = request.config.getoption("--throttle-time")
    yield
    if throttle > 0:
        time.sleep(throttle)
