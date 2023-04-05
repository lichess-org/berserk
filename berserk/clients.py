from __future__ import annotations
from time import time as now
from typing import Any, Dict, Iterator, List, Tuple, cast

import requests
from deprecated import deprecated

from . import models
from .enums import Reason
from .formats import JSON, JSON_LIST, LIJSON, NDJSON, PGN, TEXT
from .session import Requestor

__all__ = [
    "Client",
    "Account",
    "Board",
    "Bots",
    "Broadcasts",
    "Challenges",
    "Games",
    "Simuls",
    "Studies",
    "Teams",
    "Tournaments",
    "Users",
    "Messaging",
    "OAuth",
    "TV",
]

# Base URL for the API
API_URL = "https://lichess.org/"


class BaseClient:
    def __init__(self, session: requests.Session, base_url: str | None = None):
        self._r = Requestor(session, base_url or API_URL, default_fmt=JSON)


class FmtClient(BaseClient):
    """Client that can return PGN or not.

    :param session: request session, authenticated as needed
    :param base_url: base URL for the API
    :param pgn_as_default: ``True`` if PGN should be the default format
                                for game exports when possible. This defaults
                                to ``False`` and is used as a fallback when
                                ``as_pgn`` is left as ``None`` for methods that
                                support it.
    """

    def __init__(
        self,
        session: requests.Session,
        base_url: str | None = None,
        pgn_as_default: bool = False,
    ):
        super().__init__(session, base_url)
        self.pgn_as_default = pgn_as_default

    def _use_pgn(self, as_pgn: bool | None = None):
        # helper to merge default with provided arg
        return as_pgn if as_pgn is not None else self.pgn_as_default


class Client(BaseClient):
    """Main touchpoint for the API.

    All endpoints are namespaced into the clients below:

    - :class:`account <berserk.clients.Account>` - managing account information
    - :class:`bots <berserk.clients.Bots>` - performing bot operations
    - :class:`broadcasts <berserk.clients.Broadcasts>` - getting and creating
      broadcasts
    - :class:`challenges <berserk.clients.Challenges>` - using challenges
    - :class:`games <berserk.clients.Games>` - getting and exporting games
    - :class:`simuls <berserk.clients.Simuls>` - getting simultaneous
      exhibition games
    - :class:`studies <berserk.clients.Studies>` - exporting studies
    - :class:`teams <berserk.clients.Teams>` - getting information about teams
    - :class:`tournaments <berserk.clients.Tournaments>` - getting and
      creating tournaments
    - :class:`users <berserk.clients.Users>` - getting information about users
    - :class:`board <berserk.clients.Board>` - play games using a normal account
    - :class:`messaging <berserk.clients.Messaging>` - private message other players
    - :class:`tv <berserk.clients.TV>` - get information on tv channels and games

    :param session: request session, authenticated as needed
    :param base_url: base API URL to use (if other than the default)
    :param pgn_as_default: ``True`` if PGN should be the default format
                            for game exports when possible. This defaults
                            to ``False`` and is used as a fallback when
                            ``as_pgn`` is left as ``None`` for methods that
                            support it.
    """

    def __init__(
        self,
        session: requests.Session | None = None,
        base_url: str | None = None,
        pgn_as_default: bool = False,
    ):
        session = session or requests.Session()
        super().__init__(session, base_url)
        self.account = Account(session, base_url)
        self.users = Users(session, base_url)
        self.relations = Relations(session, base_url)
        self.teams = Teams(session, base_url)
        self.games = Games(session, base_url, pgn_as_default=pgn_as_default)
        self.challenges = Challenges(session, base_url)
        self.board = Board(session, base_url)
        self.bots = Bots(session, base_url)
        self.tournaments = Tournaments(session, base_url, pgn_as_default=pgn_as_default)
        self.broadcasts = Broadcasts(session, base_url)
        self.simuls = Simuls(session, base_url)
        self.studies = Studies(session, base_url)
        self.messaging = Messaging(session, base_url)

        self.oauth = OAuth(session, base_url)

        self.tv = TV(session, base_url)


class Account(BaseClient):
    """
    Client for account-related endpoints.
    """

    def get(self) -> Dict[str, Any]:
        """Get your public information.

        :return: public information about the authenticated user
        """
        path = "api/account"
        return self._r.get(path, converter=models.Account.convert)

    def get_email(self) -> str:
        """Get your email address.

        :return: email address of the authenticated user
        """
        path = "api/account/email"
        return self._r.get(path)["email"]

    def get_preferences(self) -> Dict[str, Any]:
        """Get your account preferences.

        :return: preferences of the authenticated user
        """
        path = "api/account/preferences"
        return self._r.get(path)["prefs"]

    def get_kid_mode(self) -> bool:
        """Get your kid mode status.

        :return: current kid mode status
        """
        path = "api/account/kid"
        return self._r.get(path)["kid"]

    def set_kid_mode(self, value: bool) -> bool:
        """Set your kid mode status.

        :param bool value: whether to enable or disable kid mode
        :return: success
        """
        path = "api/account/kid"
        params = {"v": value}
        return self._r.post(path, params=params)["ok"]

    def upgrade_to_bot(self) -> bool:
        """Upgrade your account to a bot account.

        Requires bot:play oauth scope. User cannot have any previously played
        games.

        :return: success
        """
        path = "api/bot/account/upgrade"
        return self._r.post(path)["ok"]


class Users(BaseClient):
    """Client for user-related endpoints."""

    def get_puzzle_activity(self, max: int | None = None) -> Iterator[Dict[str, Any]]:
        """Stream puzzle activity history starting with the most recent.

        :param int max: maximum number of entries to stream
        :return: puzzle activity history
        """
        path = "api/user/puzzle-activity"
        params = {"max": max}
        return self._r.get(
            path,
            params=params,
            fmt=NDJSON,
            stream=True,
            converter=models.PuzzleActivity.convert,
        )

    def get_realtime_statuses(
        self, *user_ids: str, with_game_ids: bool = False
    ) -> List[Dict[str, Any]]:
        """Get the online, playing, and streaming statuses of players.

        Only id and name fields are returned for offline users.

        :param user_ids: one or more user IDs (names)
        :param with_game_ids: wether to return or not the ID of the game being played
        :return: statuses of given players
        """
        path = "api/users/status"
        params = {"ids": ",".join(user_ids), "withGameIds": with_game_ids}
        return self._r.get(path, fmt=JSON_LIST, params=params)

    def get_all_top_10(self) -> Dict[str, Any]:
        """Get the top 10 players for each speed and variant.

        :return: top 10 players in each speed and variant
        """
        path = "player"
        return self._r.get(path, fmt=LIJSON)

    def get_leaderboard(self, perf_type: str, count: int = 10):
        """Get the leaderboard for one speed or variant.

        :param perf_type: speed or variant
        :type perf_type: :class:`~berserk.enums.PerfType`
        :param count: number of players to get
        :return: top players for one speed or variant
        """
        path = f"player/top/{count}/{perf_type}"
        return self._r.get(path, fmt=LIJSON)["users"]

    def get_public_data(self, username: str) -> Dict[str, Any]:
        """Get the public data for a user.

        :return: public data available for the given user
        """
        path = f"api/user/{username}"
        return self._r.get(path, converter=models.User.convert)

    def get_activity_feed(self, username: str) -> List[Dict[str, Any]]:
        """Get the activity feed of a user.

        :return: activity feed of the given user
        """
        path = f"api/user/{username}/activity"
        return self._r.get(path, fmt=JSON_LIST, converter=models.Activity.convert)

    def get_by_id(self, *usernames: str) -> List[Dict[str, Any]]:
        """Get multiple users by their IDs.

        :param usernames: one or more usernames
        :return: user data for the given usernames
        """
        path = "api/users"
        return self._r.post(
            path, data=",".join(usernames), fmt=JSON_LIST, converter=models.User.convert
        )

    @deprecated(version="0.7.0", reason="use Teams.get_members(id) instead")
    def get_by_team(self, team_id: str) -> Iterator[Dict[str, Any]]:
        """Get members of a team.

        :return: users on the given team
        """
        path = f"api/team/{team_id}/users"
        return self._r.get(path, fmt=NDJSON, stream=True, converter=models.User.convert)

    def get_live_streamers(self) -> List[Dict[str, Any]]:
        """Get basic information about currently streaming users.

        :return: users currently streaming a game
        """
        path = "streamer/live"
        return self._r.get(path, fmt=JSON_LIST)

    def get_rating_history(self, username: str) -> List[Dict[str, Any]]:
        """Get the rating history of a user.

        :return: rating history for all game types
        """
        path = f"/api/user/{username}/rating-history"
        return self._r.get(path, fmt=JSON_LIST, converter=models.RatingHistory.convert)

    def get_crosstable(
        self, user1: str, user2: str, matchup: bool = False
    ) -> List[Dict[str, Any]]:
        """Get total number of games, and current score, of any two users.

        :param user1: first user to compare
        :param user2: second user to compare
        :param matchup: Whether to get the current match data, if any
        """
        params = {"matchup": matchup}
        path = f"/api/crosstable/{user1}/{user2}"
        return self._r.get(
            path, params=params, fmt=JSON_LIST, converter=models.User.convert
        )

    def get_user_performance(self, username: str, perf: str) -> List[Dict[str, Any]]:
        """Read performance statistics of a user, for a single performance.
        Similar to the performance pages on the website
        """
        path = f"/api/user/{username}/perf/{perf}"
        return self._r.get(path, fmt=JSON_LIST, converter=models.User.convert)


class Relations(BaseClient):
    def get_users_followed(self) -> Iterator[Dict[str, Any]]:
        """Stream users you are following.

        :return: iterator over the users the given user follows
        """
        path = "/api/rel/following"
        return self._r.get(path, stream=True, fmt=NDJSON, converter=models.User.convert)

    def follow(self, username: str) -> bool:
        """Follow a player.

        :param username: user to follow
        :return: success
        """
        path = f"/api/rel/follow/{username}"
        return self._r.post(path)["ok"]

    def unfollow(self, username: str) -> bool:
        """Unfollow a player.

        :param username: user to unfollow
        :return: success
        """
        path = f"/api/rel/unfollow/{username}"
        return self._r.post(path)["ok"]


class Teams(BaseClient):
    def get_members(self, team_id: str) -> Iterator[Dict[str, Any]]:
        """Get members of a team.

        :return: users on the given team
        """
        path = f"api/team/{team_id}/users"
        return self._r.get(path, fmt=NDJSON, stream=True, converter=models.User.convert)

    def join(
        self, team_id: str, message: str | None = None, password: str | None = None
    ) -> bool:
        """Join a team.

        :param team_id: ID of a team
        :param message: Optional request message, if the team requires one
        :param password: Optional password, if the team requires one.
        :return: success
        """
        path = f"/team/{team_id}/join"
        payload = {
            "message": message,
            "password": password,
        }
        return self._r.post(path, json=payload)["ok"]

    def leave(self, team_id: str) -> bool:
        """Leave a team.

        :param team_id: ID of a team
        :return: success
        """
        path = f"/team/{team_id}/quit"
        return self._r.post(path)["ok"]

    def kick_member(self, team_id: str, user_id: str) -> bool:
        """Kick a member out of your team.

        :param team_id: ID of a team
        :param user_id: ID of a team member
        :return: success
        """
        path = f"/team/{team_id}/kick/{user_id}"
        return self._r.post(path)["ok"]


class Games(FmtClient):
    """Client for games-related endpoints."""

    def export(
        self,
        game_id: str,
        as_pgn: bool | None = None,
        moves: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
        literate: bool | None = None,
    ) -> str | Dict[str, Any]:
        """Get one finished game as PGN or JSON.

        :param game_id: the ID of the game to export
        :param as_pgn: whether to return the game in PGN format
        :param moves: whether to include the PGN moves
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in
                    the PGN moves when available
        :param opening: whether to include the opening name
        :param literate: whether to include literate the PGN
        :return: exported game, as JSON or PGN
        """
        path = f"game/export/{game_id}"
        params = {
            "moves": moves,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
            "literate": literate,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=JSON, converter=models.Game.convert
            )

    def export_ongoing_by_player(
        self,
        username: str,
        as_pgn: bool | None = None,
        moves: bool | None = None,
        pgn_in_json: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
        literate: bool | None = None,
        players: str | None = None,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Export the ongoing game, or the last game played, of a user.

        :param username: the player's username
        :param as_pgn: whether to return the game in PGN format
        :param moves: whether to include the PGN moves
        :param pgn_in_json: include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in
                           the PGN moves when available
        :param opening: whether to include the opening name
        :param literate: whether to include literate the PGN
        :param players: URL of text file containing real names and ratings for PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"api/user/{username}/current-game"
        params = {
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
            "literate": literate,
            "players": players,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, stream=True, fmt=PGN)
        else:
            return self._r.get(
                path,
                params=params,
                stream=True,
                fmt=JSON,
                converter=models.Game.convert,
            )

    def export_by_player(
        self,
        username: str,
        as_pgn: bool | None = None,
        since: int | None = None,
        until: int | None = None,
        max: int | None = None,
        vs: str | None = None,
        rated: bool | None = None,
        perf_type: str | None = None,
        color: str | None = None,
        analysed: bool | None = None,
        moves: bool | None = None,
        pgn_in_json: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
        ongoing: bool | None = None,
        finished: bool | None = None,
        players: str | None = None,
        sort: str | None = None,
        literate: bool | None = None,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Get games by player.

        :param username: which player's games to return
        :param as_pgn: whether to return the game in PGN format
        :param since: lower bound on the game timestamp
        :param until: upperbound on the game timestamp
        :param max: limit the number of games returned
        :param vs: filter by username of the opponent
        :param rated: filter by game mode (``True`` for rated, ``False``
                           for casual)
        :param perf_type: filter by speed or variant
        :type perf_type: :class:`~berserk.enums.PerfType`
        :param color: filter by the color of the player
        :type color: :class:`~berserk.enums.Color`
        :param analysed: filter by analysis availability
        :param moves: whether to include the PGN moves
        :param pgn_in_json: Include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in
                           the PGN moves when available
        :param opening: whether to include the opening name
        :param ongoing: Include ongoing games, last 3 moves omitted
        :param finished: Include finished games
        :param players: URL of text file containing real names and ratings for PGN
        :param sort: Sort the order of games
        :param literate: whether to include literate the PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"api/games/user/{username}"
        params = {
            "since": since,
            "until": until,
            "max": max,
            "vs": vs,
            "rated": rated,
            "perfType": perf_type,
            "color": color,
            "analysed": analysed,
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
            "ongoing": ongoing,
            "finished": finished,
            "players": players,
            "sort": sort,
            "literate": literate,
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

    def export_multi(
        self,
        *game_ids: str,
        as_pgn: bool | None = None,
        moves: bool | None = None,
        tags: bool | None = None,
        clocks: bool | None = None,
        evals: bool | None = None,
        opening: bool | None = None,
    ) -> Iterator[str] | Iterator[Dict[str, Any]]:
        """Get multiple games by ID.

        :param game_ids: one or more game IDs to export
        :param as_pgn: whether to return the game in PGN format
        :param moves: whether to include the PGN moves
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in
                           the PGN moves when available
        :param opening: whether to include the opening name
        :return: iterator over the exported games, as JSON or PGN
        """
        path = "games/export/_ids"
        params = {
            "moves": moves,
            "tags": tags,
            "clocks": clocks,
            "evals": evals,
            "opening": opening,
        }
        payload = ",".join(game_ids)
        if self._use_pgn(as_pgn):
            yield from self._r.post(
                path,
                params=params,
                data=payload,
                fmt=PGN,
                stream=True,
            )
        else:
            yield from self._r.post(
                path,
                params=params,
                data=payload,
                fmt=NDJSON,
                stream=True,
                converter=models.Game.convert,
            )

    def get_among_players(
        self, *usernames: str, with_current_games: bool = False
    ) -> Iterator[Dict[str, Any]]:
        """Stream the games currently being played among players.

        Note this will not include games where only one player is in the given
        list of usernames. The stream will emit an event each time a game is
        started or finished.

        :param usernames: two or more usernames
        :param with_current_games: include all current ongoing games
                                   at the beginning of the stream
        :return: iterator over all games played among the given players
        """
        path = "api/stream/games-by-users"
        params = {
            "withCurrentGames": with_current_games,
        }
        payload = ",".join(usernames)
        yield from self._r.post(
            path,
            params=params,
            data=payload,
            fmt=NDJSON,
            stream=True,
            converter=models.Game.convert,
        )

    def stream_games_by_ids(
        self, *game_ids: str, stream_id: str
    ) -> Iterator[Dict[str, Any]]:
        """Stream multiple games by ID.

        :param game_ids: one or more game IDs to stream
        :param stream_id: arbitrary stream ID that can be used later
                          to add game IDs to this stream
        :return: iterator over the stream of results
        """
        path = f"api/stream/games/{stream_id}"
        payload = ",".join(game_ids)
        yield from self._r.post(
            path, data=payload, fmt=NDJSON, stream=True, converter=models.Game.convert
        )

    def add_game_ids_to_stream(self, *game_ids: str, stream_id: str) -> bool:
        """Add new game IDs to an existing stream.

        :param stream_id: the stream ID you used to create the existing stream
        :param game_ids: one or more game IDs to stream
        :return: success
        """
        path = f"api/stream/games/{stream_id}/add"
        payload = ",".join(game_ids)
        return self._r.post(path, data=payload)["ok"]

    def get_ongoing(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get your currently ongoing games.

        :param count: number of games to get
        :return: some number of currently ongoing games
        """
        path = "api/account/playing"
        params = {"nb": count}
        return self._r.get(path, params=params)["nowPlaying"]

    @deprecated(version="0.11.12", reason="use TV.get_current_games")
    def get_tv_channels(self) -> Dict[str, Any]:
        """Get basic information about the best games being played.

        :return: best ongoing games in each speed and variant
        """
        path = "tv/channels"
        return self._r.get(path)

    def stream_game_moves(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Stream positions and moves of any ongoing game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"api/stream/game/{game_id}"
        yield from self._r.get(path, stream=True)

    def import_game(self, pgn: str) -> Dict[str, Any]:
        """Import a single game from PGN.

        :param pgn: the PGN of the game
        :return: the game ID and URL of the import
        """
        path = "api/import"
        payload = {
            "pgn": pgn,
        }
        return self._r.post(path, data=payload)


class Challenges(BaseClient):
    def create(
        self,
        username: str,
        rated: bool,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: str | None = None,
        variant: str | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Challenge another player to a game.

        :param username: username of the player to challege
        :param rated: whether or not the game will be rated
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :type color: :class:`~berserk.enums.Color`
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom intial position in FEN (variant must be
                         standard and the game cannot be rated)
        :return: challenge data
        """
        path = f"api/challenge/{username}"
        payload = {
            "rated": rated,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def create_with_accept(
        self,
        username: str,
        rated: bool,
        token: str,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: str | None = None,
        variant: str | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Start a game with another player.

        This is just like the regular challenge create except it forces the
        opponent to accept. You must provide the OAuth token of the opponent
        and it must have the challenge:write scope.

        :param username: username of the opponent
        :param rated: whether or not the game will be rated
        :param token: opponent's OAuth token
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :type color: :class:`~berserk.enums.Color`
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom intial position in FEN (variant must be
                         standard and the game cannot be rated)
        :return: game data
        """
        path = f"api/challenge/{username}"
        payload = {
            "rated": rated,
            "acceptByToken": token,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def create_ai(
        self,
        level: int = 8,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        days: int | None = None,
        color: str | None = None,
        variant: str | None = None,
        position: str | None = None,
    ) -> Dict[str, Any]:
        """Challenge AI to a game.

        :param level: level of the AI (1 to 8)
        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :type color: :class:`~berserk.enums.Color`
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: use one of the custom initial positions (variant must
                         be standard and cannot be rated)
        :return: information about the created game
        """
        path = "api/challenge/ai"
        payload = {
            "level": level,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def create_open(
        self,
        clock_limit: int | None = None,
        clock_increment: int | None = None,
        variant: str | None = None,
        position: str | None = None,
        rated: bool | None = None,
        name: str | None = None,
    ) -> Dict[str, Any]:
        """Create a challenge that any two players can join.

        :param clock_limit: clock initial time (in seconds)
        :param clock_increment: clock increment (in seconds)
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom intial position in FEN (variant must be
                         standard and the game cannot be rated)
        :param rated: Game is rated and impacts players ratings
        :param name: Optional name for the challenge, that players will see on
                     the challenge page.
        :return: challenge data
        """
        path = "api/challenge/open"
        payload = {
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "variant": variant,
            "fen": position,
            "rated": rated,
            "name": name,
        }
        return self._r.post(path, json=payload, converter=models.Tournament.convert)

    def accept(self, challenge_id: str) -> bool:
        """Accept an incoming challenge.

        :param challenge_id: id of the challenge to accept
        :return: success indicator
        """
        path = f"api/challenge/{challenge_id}/accept"
        return self._r.post(path)["ok"]

    def decline(self, challenge_id: str, reason: str = Reason.GENERIC) -> bool:
        """Decline an incoming challenge.
        :param challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        :type reason: :class:`~berserk.enums.Reason`
        :return: success indicator
        """
        path = f"api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        return self._r.post(path, json=payload)["ok"]


class Board(BaseClient):
    """Client for physical board or external application endpoints."""

    def stream_incoming_events(self) -> Iterator[Dict[str, Any]]:
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        """
        path = "api/stream/event"
        yield from self._r.get(path, stream=True)

    def seek(
        self,
        time: int,
        increment: int,
        rated: bool = False,
        variant: str = "standard",
        color: str = "random",
        rating_range: str | Tuple[int, int] | List[int] | None = None,
    ) -> float:
        """Create a public seek to start a game with a random opponent.

        :param time: intial clock time in minutes
        :param increment: clock increment in minutes
        :param rated: whether the game is rated (impacts ratings)
        :param variant: game variant to use
        :param color: color to play
        :param rating_range: range of opponent ratings
        :return: duration of the seek
        """
        if isinstance(rating_range, (list, tuple)):
            low, high = rating_range
            rating_range = f"{low}-{high}"

        path = "/api/board/seek"
        payload = {
            "rated": str(bool(rated)).lower(),
            "time": time,
            "increment": increment,
            "variant": variant,
            "color": color,
            "ratingRange": rating_range or "",
        }

        # we time the seek
        start = now()

        # just keep reading to keep the search going
        for _ in self._r.post(path, data=payload, fmt=TEXT, stream=True):
            pass

        # and return the time elapsed
        return now() - start

    def stream_game_state(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Get the stream of events for a board game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"api/board/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def make_move(self, game_id: str, move: str) -> bool:
        """Make a move in a board game.

        :param game_id: ID of a game
        :param move: move to make
        :return: success
        """
        path = f"api/board/game/{game_id}/move/{move}"
        return self._r.post(path)["ok"]

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a board game.

        :param str game_id: ID of a game
        :param str text: text of the message
        :param bool spectator: post to spectator room (else player room)
        :return: success
        :rtype: bool
        """
        path = f"api/board/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        return self._r.post(path, json=payload)["ok"]

    def abort_game(self, game_id):
        """Abort a board game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f"api/board/game/{game_id}/abort"
        return self._r.post(path)["ok"]

    def resign_game(self, game_id):
        """Resign a board game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f"api/board/game/{game_id}/resign"
        return self._r.post(path)["ok"]

    def handle_draw_offer(self, game_id, accept):
        """Create, accept, or decline a draw offer.

        To offer a draw, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a draw offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have received a
        draw offer.

        Often, it's easier to call :func:`offer_draw`, :func:`accept_draw`, or
        :func:`decline_draw`.

        :param str game_id: ID of an in-progress game
        :param bool accept: whether to accept
        :return: True if successful
        :rtype: bool
        """
        accept = "yes" if accept else "no"
        path = f"/api/board/game/{game_id}/draw/{accept}"
        return self._r.post(path)["ok"]

    def offer_draw(self, game_id):
        """Offer a draw in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_draw_offer(game_id, True)

    def accept_draw(self, game_id):
        """Accept an already offered draw in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_draw_offer(game_id, True)

    def decline_draw(self, game_id):
        """Decline an already offered draw in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_draw_offer(game_id, False)

    def handle_takeback_offer(self, game_id, accept):
        """Create, accept, or decline a takeback offer.

        To offer a takeback, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a takeback offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have received a
        takeback offer.

        Often, it's easier to call :func:`offer_takeback`, :func:`accept_takeback`, or
        :func:`decline_takeback`.

        :param str game_id: ID of an in-progress game
        :param bool accept: whether to accept
        :return: True if successful
        :rtype: bool
        """
        accept = "yes" if accept else "no"
        path = f"/api/board/game/{game_id}/takeback/{accept}"
        return self._r.post(path)["ok"]

    def offer_takeback(self, game_id):
        """Offer a takeback in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_takeback_offer(game_id, True)

    def accept_takeback(self, game_id):
        """Accept an already offered takeback in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_takeback_offer(game_id, True)

    def decline_takeback(self, game_id):
        """Decline an already offered takeback in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_takeback_offer(game_id, False)

    def claim_victory(self, game_id):
        """Claim victory when the opponent has left the game for a while.

        Generally, this should only be called once the `opponentGone` event
        is received in the board game state stream and the `claimWinInSeconds`
        time has elapsed.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        path = f'/api/board/game/{game_id}/claim-victory/'
        return self._r.post(path)['ok']


class Bots(BaseClient):
    """Client for bot-related endpoints."""

    def stream_incoming_events(self):
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        :rtype: iterator over the stream of events
        """
        path = "api/stream/event"
        yield from self._r.get(path, stream=True)

    def stream_game_state(self, game_id):
        """Get the stream of events for a bot game.

        :param str game_id: ID of a game
        :return: iterator over game states
        """
        path = f"api/bot/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def make_move(self, game_id, move):
        """Make a move in a bot game.

        :param str game_id: ID of a game
        :param str move: move to make
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/move/{move}"
        return self._r.post(path)["ok"]

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a bot game.

        :param str game_id: ID of a game
        :param str text: text of the message
        :param bool spectator: post to spectator room (else player room)
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        return self._r.post(path, json=payload)["ok"]

    def abort_game(self, game_id):
        """Abort a bot game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/abort"
        return self._r.post(path)["ok"]

    def resign_game(self, game_id):
        """Resign a bot game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f"api/bot/game/{game_id}/resign"
        return self._r.post(path)["ok"]

    def accept_challenge(self, challenge_id):
        """Accept an incoming challenge.

        :param str challenge_id: ID of a challenge
        :return: success
        :rtype: bool
        """
        path = f"api/challenge/{challenge_id}/accept"
        return self._r.post(path)["ok"]

    def decline_challenge(self, challenge_id, reason=Reason.GENERIC):
        """Decline an incoming challenge.
        :param str challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        :type reason: :class:`~berserk.enums.Reason`
        :return: success indicator
        :rtype: bool
        """
        path = f"api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        return self._r.post(path, json=payload)["ok"]


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


class Broadcasts(BaseClient):
    """Broadcast of one or more games."""

    def create(self, name, description, markdown=None, official=None):
        """Create a new broadcast.

        :param str name: name of the broadcast
        :param str description: short description
        :param str markdown: long description
        :param bool official: DO NOT USE
        :return: created tournament info
        :rtype: dict
        """
        path = "broadcast/new"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get(self, broadcast_id, slug="-"):
        """Get a broadcast by ID.

        :param str broadcast_id: ID of a broadcast
        :param str slug: slug for SEO
        :return: broadcast information
        :rtype: dict
        """
        path = f"broadcast/{slug}/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update(
        self, broadcast_id, name, description, markdown=None, official=None, slug="-"
    ):
        """Update an existing broadcast by ID.

        .. note::

            Provide all fields. Values in missing fields will be erased.

        :param str broadcast_id: ID of a broadcast
        :param str name: name of the broadcast
        :param str description: short description
        :param str markdown: long description
        :param bool official: DO NOT USE
        :param str slug: slug for SEO
        :return: updated broadcast information
        :rtype: dict
        """
        path = f"broadcast/{slug}/{broadcast_id}"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def push_pgn_update(self, broadcast_round_id, pgn_games):
        """Manually update an existing broadcast by ID.

        :param str broadcast_round_id: ID of a broadcast round
        :param list pgn_games: one or more games in PGN format
        :return: success
        :rtype: bool
        """
        path = f"broadcast/round/{broadcast_round_id}/push"
        games = "\n\n".join(g.strip() for g in pgn_games)
        return self._r.post(path, data=games)["ok"]

    def create_round(self, broadcast_id, name, sync_url=None, starts_at=None):
        """Create a new broadcast round to relay external games.

        :param str broadcast_id: broadcast tournament ID
        :param str name: Name of the broadcast round
        :param str sync_url: URL that Lichess will poll to get updates about the games.
        :param int starts_at: Timestamp in milliseconds of broadcast round start
        :return: success
        :rtype: dict
        """
        path = f"broadcast/{broadcast_id}/new"
        payload = {"name": name, "syncUrl": sync_url, "startsAt": starts_at}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round(
        self, broadcast_id, broadcast_tournament_slug="-", broadcast_round_slug="-"
    ):
        """Get information about a broadcast round

        :param broadcast_id: broadcast round id
        :param str broadcast_tournament_slug: Only used for SEO, can be safely replaced by -
        :param str broadcast_round_slug: Only used for SEO, can be safely replaced by -
        :return: broadcast round info
        :rtype: dict
        """
        path = f"broadcast/{broadcast_tournament_slug}/{broadcast_round_slug}/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update_round(self, broadcast_id, name, sync_url=None, starts_at=None):
        """Update information about a broadcast round that you created

        :param str broadcast_id: broadcast round id
        :param str name: Name of the broadcast round
        :param str sync_url: URL that Lichess will poll to get updates about the games
        :param starts_at: Timestamp in milliseconds of broadcast start
        :return: updated broadcast information
        :rtype: dict
        """
        path = f"broadcast/round/{broadcast_id}/edit"
        payload = {"name": name, "syncUrl": sync_url, "startsAt": starts_at}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)


class Simuls(BaseClient):
    """Simultaneous exhibitions - one vs many."""

    def get(self):
        """Get recently finished, ongoing, and upcoming simuls.

        :return: current simuls
        :rtype: list
        """
        path = "api/simul"
        return self._r.get(path)


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(self, study_id, chapter_id):
        """Export one chapter of a study.

        :return: chapter
        :rtype: PGN
        """
        path = f"/study/{study_id}/{chapter_id}.pgn"
        return self._r.get(path, fmt=PGN)

    def export(self, study_id):
        """Export all chapters of a study.

        :return: all chapters as PGN
        :rtype: list
        """
        path = f"/study/{study_id}.pgn"
        return self._r.get(path, fmt=PGN, stream=True)


class Messaging(BaseClient):
    def send(self, username, text):
        """Send a private message to another player.

        :param str username: the user to send the message to
        :param str text: the text to send
        """
        path = f"/inbox/{username}"
        payload = {"text": text}
        self._r.post(path, data=payload)


class OAuth(BaseClient):
    def test_tokens(self, *tokens):
        """Test the validity of up to 1000 OAuth tokens

        Valid OAuth tokens will be returned with their
        associated user ID and scopes. Invalid tokens
        will be returned as null.

        :param tokens: one or more OAuth tokens
        :return: list
        """
        path = "api/token/test"
        payload = ",".join(tokens)
        return self._r.post(path, data=payload, converter=models.OAuth.convert)


class TV(FmtClient):
    """Client for TV related endpoints."""

    def get_current_games(self):
        """Get basic information about the current TV games being played

        :return: best ongoing games in each speed and variant
        :rtype: dict
        """
        path = "api/tv/channels"
        return self._r.get(path)

    def stream_current_game(self):
        """Streams the current TV game

        :return: positions and moves of the current TV game
        :rtype: dict
        """
        path = "api/tv/feed"
        yield from self._r.get(path, stream=True)

    def get_best_ongoing(
        self,
        channel,
        as_pgn=None,
        count=None,
        moves=None,
        pgn_in_json=None,
        tags=None,
        clocks=None,
        opening=None,
    ):
        """Get a list of ongoing games for a given TV channel in PGN or NDJSON.

        :param str channel: the name of the TV channel in camel case
        :param bool as_pgn: whether to return the game in PGN format
        :param int count: the number of games to fetch [1..30]
        :param bool moves: whether to include the PGN moves
        :param bool pgn_in_json: include the full PGN within JSON response
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves
        :param bool opening: whether to include the opening name
        :return: the ongoing games of the given TV channel in PGN or NDJSON
        """
        path = f"api/tv/{channel}"
        params = {
            "nb": count,
            "moves": moves,
            "pgnInJson": pgn_in_json,
            "tags": tags,
            "clocks": clocks,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON, converter=models.TV.convert
            )
