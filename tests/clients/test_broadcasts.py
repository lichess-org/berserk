import pytest
import requests_mock

from berserk import Client
from berserk.types import BroadcastTop, PaginatedBroadcasts, BroadcastsByUser
from utils import skip_if_older_3_dot_10, validate


class TestBroadcasts:
    def test_reset_round(self):
        with requests_mock.Mocker() as mock:
            mock.post(
                "https://lichess.org/api/broadcast/round/abcdefgh/reset",
                json={"ok": True},
            )

            result = Client().broadcasts.reset_round("abcdefgh")

            assert result is None

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_top(self):
        res = Client().broadcasts.get_top(page=1, html=False)
        validate(BroadcastTop, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_search(self):
        res = Client().broadcasts.search(query="chess", page=1)
        validate(PaginatedBroadcasts, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_user(self):
        res = Client().broadcasts.get_by_user(username="lichess", page=1)
        validate(BroadcastsByUser, res)
