import pytest

from berserk import Client

from berserk.types.analysis import PositionEvaluation
from utils import validate, skip_if_older_3_dot_10


class TestAnalysis:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_cloud_evaluation(self):
        res = Client().analysis.get_cloud_evaluation(
            fen="rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
        )
        validate(PositionEvaluation, res)
