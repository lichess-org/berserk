import pytest

from berserk import Client
from berserk.types.broadcast import BroadcastTopResponse
from utils import validate


def test_get_top_valid(requests_mock):
    client = Client()

    sample = {
        "active": [],
        "upcoming": [],
        "past": {"currentPage": 1, "maxPerPage": 24, "currentPageResults": []},
    }

    requests_mock.get(
        "https://lichess.org/api/broadcast/top?page=1&html=False",
        json=sample,
    )

    res = client.broadcasts.get_top(page=1, html=False)
    validate(BroadcastTopResponse, res)
    assert res["past"]["currentPage"] == 1


def test_get_top_invalid_page_type():
    client = Client()
    with pytest.raises(ValueError):
        client.broadcasts.get_top(page="one")  # type: ignore


def test_get_top_invalid_page_value():
    client = Client()
    with pytest.raises(ValueError):
        client.broadcasts.get_top(page=0)