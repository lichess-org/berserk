import berserk
import pytest

BASE_URL = "http://bdit_lila:8080"


pytestmark = pytest.mark.skipif(
    True,
    reason="Integration tests require a running local lila instance (bdit_lila).",
)


@pytest.fixture(scope="module")
def client():
    session = berserk.TokenSession("lip_bobby")
    client = berserk.Client(session, base_url=BASE_URL)
    yield client


def test_list_studies_of_a_user(client):
    res = client.studies.get_by_user("tonyro")
    first_study = next(res)
    assert "id" in first_study
    assert "name" in first_study
    assert first_study["name"] == "Lichess Practice: Rook Endgames"
