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


class TestMasterGames:
    @pytest.mark.vcr
    def test_result(self):
        res = Client().opening_explorer.get_masters_games(
            play=["d2d4", "d7d5", "c2c4", "c7c6", "c4d5"]
        )
        assert res["white"] == 1667
        assert res["black"] == 1300
        assert res["draws"] == 4428


class TestPlayerGames:
    @pytest.mark.vcr
    @pytest.mark.default_cassette("TestPlayerGames.results.yaml")
    def test_wait_for_last_results(self):
        result = Client().opening_explorer.get_player_games(
            player="evachesss", color="white", wait_for_indexing=True
        )
        assert result["white"] == 125
        assert result["draws"] == 18
        assert result["black"] == 133

    @pytest.mark.vcr
    @pytest.mark.default_cassette("TestPlayerGames.results.yaml")
    def test_get_first_result_available(self):
        result = Client().opening_explorer.get_player_games(
            player="evachesss",
            color="white",
            wait_for_indexing=False,
        )
        assert result == {
            "white": 0,
            "draws": 0,
            "black": 0,
            "moves": [],
            "recentGames": [],
            "opening": None,
            "queuePosition": 0,
        }

    @pytest.mark.vcr
    @pytest.mark.default_cassette("TestPlayerGames.results.yaml")
    def test_stream(self):
        result = list(
            Client().opening_explorer.stream_player_games(
                player="evachesss",
                color="white",
            )
        )
        assert result[0] == {
            "white": 0,
            "draws": 0,
            "black": 0,
            "moves": [],
            "recentGames": [],
            "opening": None,
            "queuePosition": 0,
        }
        assert result[-1]["white"] == 125
        assert result[-1]["draws"] == 18
        assert result[-1]["black"] == 133
