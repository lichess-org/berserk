# -*- coding: utf-8 -*-
"""User-related endpoints."""
from typing import cast

from deprecated import deprecated

from .. import models
from ..formats import NDJSON, PGN
from . import FmtClient


class Tournaments(FmtClient):
    """Client for tournament-related endpoints."""

    def get(self) -> models.CurrentTournaments:
        """Get recently finished, ongoing, and upcoming tournaments.

        :return: current tournaments
        :rtype: list
        """
        path = "api/tournament"
        return cast(
            models.CurrentTournaments,
            self._r.get(path, converter=models.Tournament.convert_values),
        )

    def get_tournament(self, tournament_id: str, page: int = 1):
        """Get information about a tournament.
        :patam str tournament_id
        :return: tournament information
        :rtype: dict
        """
        path = f"api/tournament/{tournament_id}?page={page}"
        return self._r.get(path, converter=models.Tournament.convert)

    @deprecated(
        version="0.11.0",
        reason="use Tournaments.create_arena or Tournaments.create_swiss instead",
    )
    def create(
        self,
        clock_time,
        clock_increment,
        minutes,
        name=None,
        wait_minutes=None,
        variant=None,
        berserkable=None,
        rated=None,
        start_date=None,
        position=None,
        password=None,
        conditions=None,
    ):
        """Create a new tournament.

        .. note::
            ``wait_minutes`` is always relative to now and is overriden by
            ``start_time``.

        .. note::
            If ``name`` is left blank then one is automatically created.

        :param int clock_time: intial clock time in minutes
        :param int clock_increment: clock increment in seconds
        :param int minutes: length of the tournament in minutes
        :param str name: tournament name
        :param int wait_minutes: future start time in minutes
        :param str start_date: when to start the tournament
        :param str variant: variant to use if other than standard
        :param bool rated: whether the game affects player ratings
        :param str berserkable: whether players can use berserk
        :param str position: custom initial position in FEN
        :param str password: password (makes the tournament private)
        :param dict conditions: conditions for participation
        :return: created tournament info
        :rtype: dict
        """
        path = "api/tournament"
        payload = {
            "name": name,
            "clockTime": clock_time,
            "clockIncrement": clock_increment,
            "minutes": minutes,
            "waitMinutes": wait_minutes,
            "startDate": start_date,
            "variant": variant,
            "rated": rated,
            "position": position,
            "berserkable": berserkable,
            "password": password,
            **{f"conditions.{c}": v for c, v in (conditions or {}).items()},
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def create_arena(
        self,
        clock_time,
        clock_increment,
        minutes,
        name=None,
        wait_minutes=None,
        start_date=None,
        variant=None,
        rated=None,
        position=None,
        berserkable=None,
        streakable=None,
        hasChat=None,
        description=None,
        password=None,
        teambBattleByTeam=None,
        teamId=None,
        minRating=None,
        maxRating=None,
        nbRatedGame=None,
    ):
        """Create a new arena tournament.

        .. note::

            ``wait_minutes`` is always relative to now and is overriden by
            ``start_time``.

        .. note::

            If ``name`` is left blank then one is automatically created.

        :param int clock_time: initial clock time in minutes
        :param int clock_increment: clock increment in seconds
        :param int minutes: length of the tournament in minutes
        :param str name: tournament name
        :param int wait_minutes: future start time in minutes
        :param str start_date: when to start the tournament
        :param str variant: variant to use if other than standard
        :param bool rated: whether the game affects player ratings
        :param str position: custom initial position in FEN
        :param str berserkable: whether players can use berserk
        :param bool streakable: whether players get streaks
        :param bool hasChat: whether players can
                            discuss in a chat
        :param string description: anything you want to
                                  tell players about the tournament
        :param str password: password
        :param str teambBattleByTeam: Id of a team you lead
                                      to create a team battle
        :param string teamId: Restrict entry to members of team
        :param int minRating: Minimum rating to join
        :param int maxRating: Maximum rating to join
        :param int nbRatedGame: Min number of rated games required
        :return: created tournament info
        :rtype: dict
        """
        path = "api/tournament"
        payload = {
            "name": name,
            "clockTime": clock_time,
            "clockIncrement": clock_increment,
            "minutes": minutes,
            "waitMinutes": wait_minutes,
            "startDate": start_date,
            "variant": variant,
            "rated": rated,
            "position": position,
            "berserkable": berserkable,
            "streakable": streakable,
            "hasChat": hasChat,
            "description": description,
            "password": password,
            "teambBattleByTeam": teambBattleByTeam,
            "conditions.teamMember.teamId": teamId,
            "conditions.minRating.rating": minRating,
            "conditions.maxRating.rating": maxRating,
            "conditions.nbRatedGame.nb": nbRatedGame,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def create_swiss(
        self,
        team_id,
        clock_limit,
        clock_increment,
        nbRounds,
        name=None,
        startsAt=None,
        roundInterval=None,
        variant=None,
        description=None,
        rated=None,
        chatFor=None,
    ):
        """Create a new swiss tournament

        .. note::

            If ``name`` is left blank then one is automatically created.

        .. note::

            If ``startsAt`` is left blank then the
            tournament begins 10 minutes after creation

            :param string team_id: team Id, required for swiss tournaments
            :param int clock_limit: initial clock time in seconds
            :param int clock_increment: clock increment in seconds
            :param int nbRounds: maximum number of rounds to play
            :param string name: tournament name
            :param int startsAt: when to start tournament, in ms timestamp
            :param int roundInterval: interval between rounds in seconds
            :param string variant: variant to use if other than standard
            :param string description: tournament description
            :param bool rated: whether the game affects player ratings
            :param int chatFor: who can read and write in the chat
            :return: created tournament info
            :rtype: dict
        """
        path = f"api/swiss/new/{team_id}"

        payload = {
            "name": name,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "nbRounds": nbRounds,
            "startsAt": startsAt,
            "roundInterval": roundInterval,
            "variant": variant,
            "description": description,
            "rated": rated,
            "chatFor": chatFor,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    @deprecated(
        version="0.11.0",
        reason="use Tournaments.export_arena_games or Tournaments.export_swiss_games",
    )
    def export_games(
        self,
        id_,
        as_pgn=False,
        moves=None,
        tags=None,
        clocks=None,
        evals=None,
        opening=None,
    ):
        """Export games from a tournament.
        :param str `id_`: tournament ID
        :param bool as_pgn: whether to return PGN instead of JSON
        :param bool moves: include moves
        :param bool tags: include tags
        :param bool clocks: include clock comments in the PGN moves, when available
        :param bool evals: include analysis evalulation comments in the PGN moves, when available
        :param bool opening: include the opening name
        :return: games
        :rtype: list
        """
        path = f"api/tournament/{id_}/games"
        params = {
            "moves": moves,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.Game.convert
            )

    def export_arena_games(
        self,
        id_,
        as_pgn=False,
        moves=None,
        tags=None,
        clocks=None,
        evals=None,
        opening=None,
    ):
        """Export games from a arena tournament.

        :param str id_: tournament ID
        :param bool as_pgn: whether to return PGN instead of JSON
        :param bool moves: include moves
        :param bool tags: include tags
        :param bool clocks: include clock comments in the PGN moves, when
                            available
        :param bool evals: include analysis evalulation comments in the PGN
                           moves, when available
        :param bool opening: include the opening name
        :return: games
        :rtype: list
        """
        path = f"api/tournament/{id_}/games"
        params = {
            "moves": moves,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.Game.convert
            )

    def export_swiss_games(
        self,
        id_,
        as_pgn=False,
        moves=None,
        pgnInJson=None,
        tags=None,
        clocks=None,
        evals=None,
        opening=None,
    ):
        """Export games from a swiss tournament

        :param str id_: tournament id
        :param bool as_pgn: whether to return pgn instead of JSON
        :param bool moves: include moves
        :param bool pgnInJson: include the full PGN within the
                              JSON response, in a pgn field
        :param bool tags: include tags
        :param bool clocks: include clock comments
        :param bool evals: include analysis evaluation
                          comments in the PGN, when available
        :param bool opening: include the opening name
        :return: games
        :rtype: list
        """
        path = f"api/swiss/{id_}/games"
        params = {
            "moves:": moves,
            "pgnInJson": pgnInJson,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.Game.convert
            )

    def tournaments_by_user(self, username, nb=None, as_pgn=False):
        """Get tournaments created by a user

        :param string username: username
        :param int nb: max number of tournaments to fetch
        :param bool as_pgn: whether to return pgn instead of Json
        :return: tournaments
        :rtype: list
        """

        path = f"api/user/{username}/tournament/created"
        params = {
            "nb": nb,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.Game.convert
            )

    def arenas_by_team(self, teamId, maxT=None, as_pgn=False):
        """Get arenas created for a team

        :param string teamId: Id of the team
        :param int maxT: how many tournaments to download
        :param bool as_pgn: whether to return pgn instead of Json
        :return: tournaments
        :rtype: list
        """
        path = f"api/team/{teamId}/arena"
        params = {
            "max": maxT,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.Game.convert
            )

    def swiss_by_team(self, teamId, maxT=None, as_pgn=False):
        """Get swiss tournaments created for a team

        :param string teamId: Id of the team
        :param int maxT: how many tournaments to download
        :param bool as_pgn: whether to return pgn instead of Json
        :return: tournaments
        :rtype: list
        """
        path = f"api/team/{teamId}/swiss"
        params = {
            "max": maxT,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.Game.convert
            )

    def stream_results(self, id_, limit=None):
        """Stream the results of a tournament.

        Results are the players of a tournament with their scores and
        performance in rank order. Note that results for ongoing
        tournaments can be inconsistent due to ranking changes.

        :param str id_: tournament ID
        :param int limit: maximum number of results to stream
        :return: iterator over the stream of results
        :rtype: iter
        """
        path = f"api/tournament/{id_}/results"
        params = {"nb": limit}
        return self._r.get(path, params=params, stream=True)

    def stream_by_creator(self, username):
        """Stream the tournaments created by a player.

        :param str username: username of the player
        :return: tournaments
        :rtype: iter
        """
        path = f"api/user/{username}/tournament/created"
        return self._r.get(path, stream=True)
