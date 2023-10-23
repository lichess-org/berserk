from __future__ import annotations

from typing import Iterator, Any, Dict, List, cast

from .. import models
from ..formats import NDJSON, NDJSON_LIST, PGN
from .base import FmtClient
from ..types.tournament import TournamentInfo


class Tournaments(FmtClient):
    """Client for tournament-related endpoints."""

    def get(self) -> models.CurrentTournaments:
        """Get recently finished, ongoing, and upcoming tournaments.

        :return: current tournaments
        """
        path = "/api/tournament"
        return cast(
            models.CurrentTournaments,
            self._r.get(path, converter=models.Tournament.convert_values),
        )

    def get_tournament(self, tournament_id: str, page: int = 1):
        """Get information about a tournament.

        :param tournament_id
        :return: tournament information
        """
        path = f"/api/tournament/{tournament_id}?page={page}"
        return self._r.get(path, converter=models.Tournament.convert)

    def create_arena(
        self,
        clockTime: int,
        clockIncrement: int,
        minutes: int,
        name: str | None = None,
        wait_minutes: int | None = None,
        startDate: int | None = None,
        variant: str | None = None,
        rated: bool | None = None,
        position: str | None = None,
        berserkable: bool | None = None,
        streakable: bool | None = None,
        hasChat: bool | None = None,
        description: str | None = None,
        password: str | None = None,
        teamBattleByTeam: str | None = None,
        teamId: str | None = None,
        minRating: int | None = None,
        maxRating: int | None = None,
        nbRatedGame: int | None = None,
    ) -> Dict[str, Any]:
        """Create a new arena tournament.

        .. note::

            ``wait_minutes`` is always relative to now and is overridden by
            ``start_time``.

        .. note::

            If ``name`` is left blank then one is automatically created.

        :param clockTime: initial clock time in minutes
        :param clockIncrement: clock increment in seconds
        :param minutes: length of the tournament in minutes
        :param name: tournament name
        :param wait_minutes: future start time in minutes
        :param startDate: when to start the tournament (timestamp in milliseconds)
        :param variant: variant to use if other than standard
        :param rated: whether the game affects player ratings
        :param position: custom initial position in FEN
        :param berserkable: whether players can use berserk
        :param streakable: whether players get streaks
        :param hasChat: whether players can discuss in a chat
        :param description: anything you want to tell players about the tournament
        :param password: password
        :param teamBattleByTeam: Id of a team you lead to create a team battle
        :param teamId: Restrict entry to members of team
        :param minRating: Minimum rating to join
        :param maxRating: Maximum rating to join
        :param nbRatedGame: Min number of rated games required
        :return: created tournament info
        """
        path = "/api/tournament"
        payload = {
            "name": name,
            "clockTime": clockTime,
            "clockIncrement": clockIncrement,
            "minutes": minutes,
            "waitMinutes": wait_minutes,
            "startDate": startDate,
            "variant": variant,
            "rated": rated,
            "position": position,
            "berserkable": berserkable,
            "streakable": streakable,
            "hasChat": hasChat,
            "description": description,
            "password": password,
            "teamBattleByTeam": teamBattleByTeam,
            "conditions.teamMember.teamId": teamId,
            "conditions.minRating.rating": minRating,
            "conditions.maxRating.rating": maxRating,
            "conditions.nbRatedGame.nb": nbRatedGame,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def create_swiss(
        self,
        teamId: str,
        clockLimit: int,
        clockIncrement: int,
        nbRounds: int,
        name: str | None = None,
        startsAt: int | None = None,
        roundInterval: int | None = None,
        variant: str | None = None,
        description: str | None = None,
        rated: bool | None = None,
        chatFor: int | None = None,
    ) -> Dict[str, Any]:
        """Create a new swiss tournament.

        .. note::

            If ``name`` is left blank then one is automatically created.

        .. note::

            If ``startsAt`` is left blank then the tournament begins 10 minutes after
            creation

        :param teamId: team Id, required for swiss tournaments
        :param clockLimit: initial clock time in seconds
        :param clockIncrement: clock increment in seconds
        :param nbRounds: maximum number of rounds to play
        :param name: tournament name
        :param startsAt: when to start tournament (timestamp in milliseconds)
        :param roundInterval: interval between rounds in seconds
        :param variant: variant to use if other than standard
        :param description: tournament description
        :param rated: whether the game affects player ratings
        :param chatFor: who can read and write in the chat
        :return: created tournament info
        """
        path = f"/api/swiss/new/{teamId}"

        payload = {
            "name": name,
            "clock.limit": clockLimit,
            "clock.increment": clockIncrement,
            "nbRounds": nbRounds,
            "startsAt": startsAt,
            "roundInterval": roundInterval,
            "variant": variant,
            "description": description,
            "rated": rated,
            "chatFor": chatFor,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def export_arena_games(
        self,
        id: str,
        as_pgn: bool | None = None,
        moves: bool = True,
        tags: bool = True,
        clocks: bool = False,
        evals: bool = True,
        opening: bool = False,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Export games from a arena tournament.

        :param id: tournament ID
        :param as_pgn: whether to return PGN instead of JSON
        :param moves: include moves
        :param tags: include tags
        :param clocks: include clock comments in the PGN moves, when available
        :param evals: include analysis evalulation comments in the PGN moves, when
            available
        :param opening: include the opening name
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"/api/tournament/{id}/games"
        params = {
            "moves": moves,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            yield from self._r.get(path, params=params, fmt=PGN, stream=True)
        else:
            yield from self._r.get(
                path,
                params=params,
                fmt=NDJSON,
                stream=True,
                converter=models.Game.convert,
            )

    def export_swiss_games(
        self,
        id: str,
        as_pgn: bool | None = None,
        moves: bool = True,
        pgnInJson: bool = False,
        tags: bool = True,
        clocks: bool = False,
        evals: bool = True,
        opening: bool = False,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Export games from a swiss tournament.

        :param id: tournament id
        :param as_pgn: whether to return pgn instead of JSON
        :param moves: include moves
        :param pgnInJson: include the full PGN within the JSON response, in a pgn field
        :param tags: include tags
        :param clocks: include clock comments
        :param evals: include analysis evaluation comments in the PGN, when available
        :param opening: include the opening name
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"/api/swiss/{id}/games"
        params = {
            "moves:": moves,
            "pgnInJson": pgnInJson,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            yield from self._r.get(path, params=params, fmt=PGN, stream=True)
        else:
            yield from self._r.get(
                path,
                params=params,
                fmt=NDJSON,
                stream=True,
                converter=models.Game.convert,
            )

    def tournaments_by_user(
        self, username: str, nb: int | None = None
    ) -> List[Dict[str, Any]]:
        """Get tournaments created by a user.

        :param username: username
        :param nb: max number of tournaments to fetch
        :return: tournaments
        """

        path = f"/api/user/{username}/tournament/created"
        params = {
            "nb": nb,
        }
        return self._r.get(
            path, params=params, fmt=NDJSON_LIST, converter=models.Game.convert
        )

    def arenas_by_team(
        self, teamId: str, maxT: int | None = None
    ) -> List[Dict[str, Any]]:
        """Get arenas created for a team.

        :param teamId: Id of the team
        :param maxT: how many tournaments to download
        :return: tournaments
        """
        path = f"/api/team/{teamId}/arena"
        params = {
            "max": maxT,
        }
        return self._r.get(
            path, params=params, fmt=NDJSON_LIST, converter=models.Game.convert
        )

    def swiss_by_team(
        self, teamId: str, maxT: int | None = None
    ) -> List[Dict[str, Any]]:
        """Get swiss tournaments created for a team.

        :param teamId: Id of the team
        :param maxT: how many tournaments to download
        :return: tournaments
        """
        path = f"/api/team/{teamId}/swiss"
        params = {
            "max": maxT,
        }
        return self._r.get(
            path, params=params, fmt=NDJSON_LIST, converter=models.Game.convert
        )

    def stream_results(
        self, id: str, limit: int | None = None
    ) -> Iterator[Dict[str, Any]]:
        """Stream the results of a tournament.

        Results are the players of a tournament with their scores and performance in
        rank order. Note that results for ongoing tournaments can be inconsistent due to
        ranking changes.

        :param id: tournament ID
        :param limit: maximum number of results to stream
        :return: iterator over the results
        """
        path = f"/api/tournament/{id}/results"
        params = {"nb": limit}
        yield from self._r.get(path, params=params, stream=True)

    def stream_by_creator(self, username: str) -> Iterator[Dict[str, Any]]:
        """Stream the tournaments created by a player.

        :param username: username of the player
        :return: iterator over the tournaments
        """
        path = f"/api/user/{username}/tournament/created"
        yield from self._r.get(path, stream=True)

    def get_swiss_info_by_id(self, swiss_id: str) -> TournamentInfo:
        """Get detailed info about a Swiss tournament.

        :param swiss_id: the Swiss tournament ID.
        :return: detailed info about a Swiss tournament
        """
        path = f"/api/swiss/{swiss_id}"
        return cast(TournamentInfo, self._r.get(path))

    def update_swiss(
        self,
        tournamentId: str,
        clockLimit: int,
        clockIncrement: int,
        nbRounds: int,
        startsAt: int | None = None,
        roundInterval: int | None = None,
        variant: str | None = None,
        description: str | None = None,
        name: str | None = None,
        rated: bool | None = True,
        password: str | None = None,
        forbiddenPairings: str | None = None,
        manualPairings: str | None = None,
        chatFor: int | None = 20,
        minRating: int | None = None,
        maxRating: int | None = None,
        nbRatedGame: int | None = None,
        allowList: str | None = None,
    ) -> Dict[str, TournamentInfo]:
        """Updata a swiss tournament.

        :param tournamentId : The unique identifier of the tournament to be updated.
        :param clockLimit : The time limit for each player's clock.
        :param clockIncrement : The time increment added to a player's clock after each move.
        :param nbRounds : The number of rounds in the tournament.
        :param startsAt : The start time of the tournament in Unix timestamp format.
        :param roundInterval :The time interval between rounds in minutes.
        :param variant :The chess variant of the tournament.
        :param description : A description of the tournament.
        :param name : The name of the tournament.
        :param rated : Whether the tournament is rated.
        :param password : A password to access the tournament.
        :param forbiddenPairings : Specify forbidden pairings in the tournament.
        :param manualPairings : Specify manual pairings for the tournament.
        :param chatFor :The duration for which the chat is available in minutes.
        :param minRating : The minimum rating required to participate in the tournament.
        :param maxRating : The maximum rating allowed to participate in the tournament.
        :param nbRatedGame : The number of rated games required for participation.
        :param allowList : Specify an allow list for the tournament.
        :return A dictionary containing information about the updated Swiss tournament.
        """
        path = f"/api/swiss/{tournamentId}/edit/"

        payload = {
            "name": name,
            "clock.limit": clockLimit,
            "clock.increment": clockIncrement,
            "nbRounds": nbRounds,
            "startsAt": startsAt,
            "roundInterval": roundInterval,
            "variant": variant,
            "description": description,
            "rated": rated,
            "password": password,
            "forbiddenPairings": forbiddenPairings,
            "manualPairings": manualPairings,
            "conditions.minRating.rating": minRating,
            "conditions.maxRating.rating": maxRating,
            "conditions.nbRatedGame.nb": nbRatedGame,
            "conditions.allowList": allowList,
            "chatFor": chatFor,
        }
        return self._r.post(path, json=payload)
