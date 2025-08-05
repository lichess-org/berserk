import pytest
from berserk import Client
from berserk.types import Difficulty
from utils import skip_if_older_3_dot_10


class TestPuzzles:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_next_puzzle(self):
        """Ensure we can fetch a new puzzle using /api/puzzle/next"""
        client = Client()
        res = client.puzzles.get_next(difficulty=Difficulty.NORMAL)

        assert isinstance(res, dict)
        assert "puzzle" in res
        assert "game" in res
        assert "id" in res["puzzle"]

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_next_puzzle_with_angle(self):
        """Ensure we can fetch a new puzzle with an angle filter"""
        client = Client()
        res = client.puzzles.get_next(angle="endgame")

        assert isinstance(res, dict)
        assert "puzzle" in res
        assert "game" in res
        assert "id" in res["puzzle"]
