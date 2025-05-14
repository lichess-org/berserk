import pytest
from typing import List
from berserk import Client
from berserk.types.fide import FidePlayer
from utils import validate, skip_if_older_3_dot_10


class TestFide:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_search_players(self):
        res = Client().fide.search_players("Erigaisi")
        validate(List[FidePlayer], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_player(self):
        res = Client().fide.get_player(35009192)
        validate(FidePlayer, res)
        assert res["name"] == "Erigaisi Arjun"
