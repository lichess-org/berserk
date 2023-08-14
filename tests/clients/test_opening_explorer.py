import pytest
import requests_mock

from berserk import Client, OpeningStatistic

from utils import validate, skip_if_older_3_dot_10


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_result(self):
        """Verify that the response matches the typed-dict"""
        res = Client().opening_explorer.get_lichess_games(
            variant="standard",
            speeds=["blitz", "rapid", "classical"],
            ratings=["2200", "2500"],
            position="rnbqkbnr/ppp2ppp/8/3pp3/4P3/2NP4/PPP2PPP/R1BQKBNR b KQkq - 0 1",
        )
        validate(OpeningStatistic, res)

    def test_correct_speed_params(self):
        """The test verify that speeds parameter are passed correctly in query params"""
        with requests_mock.Mocker() as m:
            m.get(
                "https://explorer.lichess.ovh/lichess?variant=standard&speeds=rapid%2Cclassical",
                json={},
            )
            Client().opening_explorer.get_lichess_games(speeds=["rapid", "classical"])

    def test_correct_rating_params(self):
        """The test verify that ratings parameter are passed correctly in query params"""
        with requests_mock.Mocker() as m:
            m.get(
                "https://explorer.lichess.ovh/lichess?variant=standard&ratings=1200%2C1400",
                json={},
            )
            Client().opening_explorer.get_lichess_games(ratings=["1200", "1400"])
