from pathlib import Path

import vcr
import pytest


@pytest.fixture(scope="function")
def stored_requests(request) -> vcr.VCR:
    test_filename, _, _ = request.node.location

    parent_directory = Path(test_filename).parent
    cassette_directory = parent_directory / Path("casettes")

    vcr_config = vcr.VCR(
        cassette_library_dir=str(cassette_directory), record_mode="none"
    )

    yield vcr_config
