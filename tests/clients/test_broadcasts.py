import pytest

from berserk import Client
from berserk.types.broadcast import BroadcastTopResponse
from utils import skip_if_older_3_dot_10, validate


@skip_if_older_3_dot_10
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
