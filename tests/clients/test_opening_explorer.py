import pytest
import requests_mock

from berserk.clients import Client


class TestLichessGames:
    @pytest.mark.vcr
    def test_result(self):
        client = Client()
        res = client.opening_explorer.get_lichess_games(
            variant="standard",
            speeds=["blitz", "rapid", "classical"],
            ratings=["2200", "2500"],
            position="rnbqkbnr/ppp2ppp/8/3pp3/4P3/2NP4/PPP2PPP/R1BQKBNR b KQkq - 0 1",
        )
        assert res["white"] == 1212
        assert res["black"] == 1406
        assert res["draws"] == 160

    def test_correct_speed_params(self):
        """The test verify that speeds parameter are passed correctly in query params"""
        client = Client()

        with requests_mock.Mocker() as m:
            m.get(
                "https://explorer.lichess.ovh/lichess?variant=standard&speeds=rapid%2Cclassical",
                json={},
            )
            client.opening_explorer.get_lichess_games(speeds=["rapid", "classical"])

    def test_correct_rating_params(self):
        """The test verify that ratings parameter are passed correctly in query params"""
        client = Client()

        with requests_mock.Mocker() as m:
            m.get(
                "https://explorer.lichess.ovh/lichess?variant=standard&ratings=1200%2C1400",
                json={},
            )
            client.opening_explorer.get_lichess_games(ratings=["1200", "1400"])
