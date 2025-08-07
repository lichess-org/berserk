import pytest

from berserk import Client, Puzzle
from utils import validate, skip_if_older_3_dot_10


class TestLichessPuzzles:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_daily(self):
        """Test getting the daily puzzle (no authentication required)."""
        res = Client().puzzles.get_daily()
        validate(Puzzle, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_puzzle_by_id(self):
        """Test getting a puzzle by its ID (no authentication required)."""
        # Using a known puzzle ID for testing
        puzzle_id = "ponnQ"  # This is a common example puzzle ID from Lichess
        res = Client().puzzles.get(puzzle_id)
        validate(Puzzle, res)
        assert res["id"] == puzzle_id