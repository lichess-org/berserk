import pytest

from berserk import Client, PuzzleData, PuzzleRace
from utils import validate, skip_if_older_3_dot_10


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_puzzle_next(self):
        """Validate that the response matches the typed-dict"""
        res = Client().puzzles.get_next(angle="anastasiaMate", difficulty="hardest")
        validate(PuzzleData, res)
