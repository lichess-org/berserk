import pytest
import requests_mock
from berserk import (
    Client,
    OpeningStatistic,
    MastersOpeningStatistic,
    PlayerOpeningStatistic,
)
from typing import List

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
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_result(self):
        """Verify that the response matches the typed-dict"""
        res = Client().opening_explorer.get_masters_games(
            play=["d2d4", "d7d5", "c2c4", "c7c6", "c4d5"]
        )
        validate(MastersOpeningStatistic, res)

    @pytest.mark.vcr
    def test_export(self):
        res = Client().opening_explorer.get_otb_master_game("LSVO85Cp")
        assert (
            res
            == """[Event "3rd Norway Chess 2015"]
[Site "Stavanger NOR"]
[Date "2015.06.17"]
[Round "2.4"]
[White "Caruana, F."]
[Black "Carlsen, M."]
[Result "1-0"]
[WhiteElo "2805"]
[BlackElo "2876"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O Nxe4 5. d4 Nd6 6. Bxc6 dxc6 7. dxe5 Nf5 8. Qxd8+ Kxd8 9. h3 h6 10. Rd1+ Ke8 11. Nc3 Ne7 12. b3 Bf5 13. Nd4 Bh7 14. Bb2 Rd8 15. Nce2 Nd5 16. c4 Nb4 17. Nf4 Rg8 18. g4 Na6 19. Nf5 Nc5 20. Rxd8+ Kxd8 21. Rd1+ Kc8 22. Ba3 Ne6 23. Nxe6 Bxa3 24. Nexg7 Bf8 25. e6 Bxf5 26. Nxf5 fxe6 27. Ng3 Be7 28. Kg2 Rf8 29. Rd3 Rf7 30. Nh5 Bd6 31. Rf3 Rh7 32. Re3 Re7 33. f4 Ba3 34. Kf3 Bb2 35. Re2 Bc3 36. g5 Kd7 37. Kg4 Re8 38. Ng3 Rh8 39. h4 b6 40. h5 c5 41. g6 Re8 42. f5 exf5+ 43. Kf4 Rh8 44. Nxf5 Bf6 45. Rg2 1-0
"""
        )


class TestPlayerGames:
    @pytest.mark.vcr
    @pytest.mark.default_cassette("TestPlayerGames.results.yaml")
    def test_wait_for_last_results(self):
        result = Client().opening_explorer.get_player_games(
            player="evachesss", color="white", wait_for_indexing=True
        )
        validate(PlayerOpeningStatistic, result)

    @pytest.mark.vcr
    @pytest.mark.default_cassette("TestPlayerGames.results.yaml")
    def test_get_first_result_available(self):
        result = Client().opening_explorer.get_player_games(
            player="evachesss",
            color="white",
            wait_for_indexing=False,
        )
        validate(PlayerOpeningStatistic, result)

    @pytest.mark.vcr
    @pytest.mark.default_cassette("TestPlayerGames.results.yaml")
    def test_stream(self):
        iterator = Client().opening_explorer.stream_player_games(
            player="evachesss",
            color="white",
        )
        # Just test that the stream yields at least one result
        result = next(iterator)
        validate(PlayerOpeningStatistic, result)
