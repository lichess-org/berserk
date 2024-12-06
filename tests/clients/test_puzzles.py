import pytest

from berserk import Client
from typing import List, Dict, Any, Iterator
from utils import validate, skip_if_older_3_dot_10

from berserk.types.puzzles import PuzzleRace


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_next(self):
        res = Client().puzzles.get_next("mix", "normal")
        validate(Dict[str, Any], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_storm_dashboard(self):
        res = Client().puzzles.get_storm_dashboard("Chess700800", 0)
        validate(Dict[str, Any], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get(self):
        res = Client().puzzles.get("BG3VT")
        validate(Dict[str, Any], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_daily(self):
        res = Client().puzzles.get_daily()
        validate(Dict[str, Any], res)
