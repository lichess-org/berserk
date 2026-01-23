import pytest

from berserk import Client
from berserk.types.puzzles import PuzzleData, PuzzleReplayData
from utils import validate, skip_if_older_3_dot_10


class TestPuzzles:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_next(self):
        """Validate that the response matches the typed-dict"""
        res = Client().puzzles.get_next(angle="anastasiaMate", difficulty="hardest")
        validate(PuzzleData, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_puzzles_to_replay(self):
        res = Client().puzzles.get_puzzles_to_replay(30, "mix")
        validate(PuzzleReplayData, res)
