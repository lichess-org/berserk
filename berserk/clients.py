from __future__ import annotations

from time import time as now
from typing import Any, Dict, Iterator, List, Literal, Tuple, cast

import requests
from deprecated import deprecated

from . import models
from .enums import Reason
from .formats import JSON, JSON_LIST, LIJSON, NDJSON, NDJSON_LIST, PGN, TEXT
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
    "Puzzles",
    "Messaging",
    "OAuth",
    "TV",
]

# Base URL for the API
API_URL = "https://lichess.org"
TABLEBASE_URL = "https://tablebase.lichess.ovh"


class BaseClient:
    def __init__(self, session: requests.Session, base_url: str | None = None):
        self._r = Requestor(session, base_url or API_URL, default_fmt=JSON)


class FmtClient(BaseClient):
    """Client that can return PGN or not.

    :param session: request session, authenticated as needed
    :param base_url: base URL for the API
    :param pgn_as_default: ``True`` if PGN should be the default format for game exports
        when possible. This defaults to ``False`` and is used as a fallback when
        ``as_pgn`` is left as ``None`` for methods that support it.
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
    - :class:`broadcasts <berserk.clients.Broadcasts>` - getting and creating broadcasts
    - :class:`challenges <berserk.clients.Challenges>` - using challenges
    - :class:`games <berserk.clients.Games>` - getting and exporting games
    - :class:`simuls <berserk.clients.Simuls>` - getting simultaneous exhibition games
    - :class:`studies <berserk.clients.Studies>` - exporting studies
    - :class:`teams <berserk.clients.Teams>` - getting information about teams
    - :class:`tournaments <berserk.clients.Tournaments>` - getting and creating
        tournaments
    - :class:`users <berserk.clients.Users>` - getting information about users
    - :class:`board <berserk.clients.Board>` - play games using a normal account
    - :class:`messaging <berserk.clients.Messaging>` - private message other players
    - :class:`tv <berserk.clients.TV>` - get information on tv channels and games
    - :class:`tablebase <berserk.clients.Tablebase>` - lookup endgame tablebase

    :param session: request session, authenticated as needed
    :param base_url: base API URL to use (if other than the default)
    :param pgn_as_default: ``True`` if PGN should be the default format for game exports
        when possible. This defaults to ``False`` and is used as a fallback when
        ``as_pgn`` is left as ``None`` for methods that support it.
    :param tablebase_url: URL for tablebase lookups
    """

    def __init__(
        self,
        session: requests.Session | None = None,
        base_url: str | None = None,
        pgn_as_default: bool = False,
        *,
        tablebase_url: str | None = None,
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
        self.puzzles = Puzzles(session, base_url)
        self.oauth = OAuth(session, base_url)
        self.tv = TV(session, base_url)
        self.tablebase = Tablebase(session, tablebase_url or TABLEBASE_URL)


class Account(BaseClient):
    """Client for account-related endpoints."""

    def get(self) -> Dict[str, Any]:
        """Get your public information.

        :return: public information about the authenticated user
        """
        path = "/api/account"
        return self._r.get(path, converter=models.Account.convert)

    def get_email(self) -> str:
        """Get your email address.

        :return: email address of the authenticated user
        """
        path = "/api/account/email"
        return self._r.get(path)["email"]

    def get_preferences(self) -> Dict[str, Any]:
        """Get your account preferences.

        :return: preferences of the authenticated user
        """
        path = "/api/account/preferences"
        return self._r.get(path)["prefs"]

    def get_kid_mode(self) -> bool:
        """Get your kid mode status.

        :return: current kid mode status
        """
        path = "/api/account/kid"
        return self._r.get(path)["kid"]

    def set_kid_mode(self, value: bool):
        """Set your kid mode status.

        :param bool value: whether to enable or disable kid mode
        """
        path = "/api/account/kid"
        params = {"v": value}
        self._r.post(path, params=params)

    def upgrade_to_bot(self):
        """Upgrade your account to a bot account.

        Requires bot:play oauth scope. User cannot have any previously played games.
        """
        path = "/api/bot/account/upgrade"
        self._r.post(path)


class Users(BaseClient):
    """Client for user-related endpoints."""

    @deprecated(reason="Use Puzzles.get_puzzle_activity instead", version="0.12.6")
    def get_puzzle_activity(self, max: int | None = None) -> Iterator[Dict[str, Any]]:
        """Stream puzzle activity history of the authenticated user, starting with the most recent activity.

        :param max: maximum number of entries to stream. defaults to all activity
        :return: stream of puzzle activity history
        """
        path = "/api/puzzle/activity"
        params = {"max": max}
        yield from self._r.get(
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
        path = "/api/users/status"
        params = {"ids": ",".join(user_ids), "withGameIds": with_game_ids}
        return self._r.get(path, fmt=JSON_LIST, params=params)

    def get_all_top_10(self) -> Dict[str, Any]:
        """Get the top 10 players for each speed and variant.

        :return: top 10 players in each speed and variant
        """
        path = "/player"
        return self._r.get(path, fmt=LIJSON)

    def get_leaderboard(self, perf_type: str, count: int = 10):
        """Get the leaderboard for one speed or variant.

        :param perf_type: speed or variant
        :type perf_type: :class:`~berserk.enums.PerfType`
        :param count: number of players to get
        :return: top players for one speed or variant
        """
        path = f"/player/top/{count}/{perf_type}"
        return self._r.get(path, fmt=LIJSON)["users"]

    def get_public_data(self, username: str) -> Dict[str, Any]:
        """Get the public data for a user.

        :return: public data available for the given user
        """
        path = f"/api/user/{username}"
        return self._r.get(path, converter=models.User.convert)

    def get_activity_feed(self, username: str) -> List[Dict[str, Any]]:
        """Get the activity feed of a user.

        :return: activity feed of the given user
        """
        path = f"/api/user/{username}/activity"
        return self._r.get(path, fmt=JSON_LIST, converter=models.Activity.convert)

    def get_by_id(self, *usernames: str) -> List[Dict[str, Any]]:
        """Get multiple users by their IDs.

        :param usernames: one or more usernames
        :return: user data for the given usernames
        """
        path = "/api/users"
        return self._r.post(
            path, data=",".join(usernames), fmt=JSON_LIST, converter=models.User.convert
        )

    def get_live_streamers(self) -> List[Dict[str, Any]]:
        """Get basic information about currently streaming users.

        :return: users currently streaming a game
        """
        path = "/streamer/live"
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
        yield from self._r.get(
            path, stream=True, fmt=NDJSON, converter=models.User.convert
        )

    def follow(self, username: str):
        """Follow a player.

        :param username: user to follow
        """
        path = f"/api/rel/follow/{username}"
        self._r.post(path)

    def unfollow(self, username: str):
        """Unfollow a player.

        :param username: user to unfollow
        """
        path = f"/api/rel/unfollow/{username}"
        self._r.post(path)


class Teams(BaseClient):
    def get_members(self, team_id: str) -> Iterator[Dict[str, Any]]:
        """Get members of a team.

        :return: users on the given team
        """
        path = f"/api/team/{team_id}/users"
        yield from self._r.get(
            path, fmt=NDJSON, stream=True, converter=models.User.convert
        )

    def join(
        self, team_id: str, message: str | None = None, password: str | None = None
    ) -> None:
        """Join a team.

        :param team_id: ID of a team
        :param message: Optional request message, if the team requires one
        :param password: Optional password, if the team requires one.
        """
        path = f"/team/{team_id}/join"
        payload = {
            "message": message,
            "password": password,
        }
        self._r.post(path, json=payload)

    def leave(self, team_id: str) -> None:
        """Leave a team.

        :param team_id: ID of a team
        """
        path = f"/team/{team_id}/quit"
        self._r.post(path)

    def kick_member(self, team_id: str, user_id: str) -> None:
        """Kick a member out of your team.

        :param team_id: ID of a team
        :param user_id: ID of a team member
        """
        path = f"/team/{team_id}/kick/{user_id}"
        self._r.post(path)


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
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :param literate: whether to include literate the PGN
        :return: exported game, as JSON or PGN
        """
        path = f"/game/export/{game_id}"
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
            return self._r.get(path, params=params, converter=models.Game.convert)

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
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :param literate: whether to include literate the PGN
        :param players: URL of text file containing real names and ratings for PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"/api/user/{username}/current-game"
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
            yield from self._r.get(path, params=params, stream=True, fmt=PGN)
        else:
            yield from self._r.get(
                path,
                params=params,
                stream=True,
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
        :param rated: filter by game mode (``True`` for rated, ``False`` for casual)
        :param perf_type: filter by speed or variant
        :type perf_type: :class:`~berserk.enums.PerfType`
        :param color: filter by the color of the player
        :type color: :class:`~berserk.enums.Color`
        :param analysed: filter by analysis availability
        :param moves: whether to include the PGN moves
        :param pgn_in_json: Include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :param ongoing: Include ongoing games, last 3 moves omitted
        :param finished: Include finished games
        :param players: URL of text file containing real names and ratings for PGN
        :param sort: Sort the order of games
        :param literate: whether to include literate the PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f"/api/games/user/{username}"
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
        :param evals: whether to include analysis evaluation comments in the PGN moves
            when available
        :param opening: whether to include the opening name
        :return: iterator over the exported games, as JSON or PGN
        """
        path = "/api/games/export/_ids"
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
        :param with_current_games: include all current ongoing games at the beginning of
            the stream
        :return: iterator over all games played among the given players
        """
        path = "/api/stream/games-by-users"
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
        :param stream_id: arbitrary stream ID that can be used later to add game IDs to
            this stream
        :return: iterator over the stream of results
        """
        path = f"/api/stream/games/{stream_id}"
        payload = ",".join(game_ids)
        yield from self._r.post(
            path, data=payload, fmt=NDJSON, stream=True, converter=models.Game.convert
        )

    def add_game_ids_to_stream(self, *game_ids: str, stream_id: str) -> None:
        """Add new game IDs to an existing stream.

        :param stream_id: the stream ID you used to create the existing stream
        :param game_ids: one or more game IDs to stream
        """
        path = f"/api/stream/games/{stream_id}/add"
        payload = ",".join(game_ids)
        self._r.post(path, data=payload)

    def get_ongoing(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get your currently ongoing games.

        :param count: number of games to get
        :return: some number of currently ongoing games
        """
        path = "/api/account/playing"
        params = {"nb": count}
        return self._r.get(path, params=params)["nowPlaying"]

    def stream_game_moves(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Stream positions and moves of any ongoing game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"/api/stream/game/{game_id}"
        yield from self._r.get(path, stream=True)

    def import_game(self, pgn: str) -> Dict[str, Any]:
        """Import a single game from PGN.

        :param pgn: the PGN of the game
        :return: the game ID and URL of the import
        """
        path = "/api/import"
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
        :param position: custom initial position in FEN (variant must be standard and
            the game cannot be rated)
        :return: challenge data
        """
        path = f"/api/challenge/{username}"
        payload = {
            "rated": rated,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload)

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
        :param position: custom initial position in FEN (variant must be standard and
            the game cannot be rated)
        :return: game data
        """
        path = f"/api/challenge/{username}"
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
        return self._r.post(path, json=payload)

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
        :param position: use one of the custom initial positions (variant must be
            standard and cannot be rated)
        :return: information about the created game
        """
        path = "/api/challenge/ai"
        payload = {
            "level": level,
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "days": days,
            "color": color,
            "variant": variant,
            "fen": position,
        }
        return self._r.post(path, json=payload)

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
        :param position: custom initial position in FEN (variant must be standard and
            the game cannot be rated)
        :param rated: Game is rated and impacts players ratings
        :param name: Optional name for the challenge, that players will see on
                     the challenge page.
        :return: challenge data
        """
        path = "/api/challenge/open"
        payload = {
            "clock.limit": clock_limit,
            "clock.increment": clock_increment,
            "variant": variant,
            "fen": position,
            "rated": rated,
            "name": name,
        }
        return self._r.post(path, json=payload)

    def accept(self, challenge_id: str) -> None:
        """Accept an incoming challenge.

        :param challenge_id: id of the challenge to accept
        """
        path = f"/api/challenge/{challenge_id}/accept"
        self._r.post(path)

    def decline(self, challenge_id: str, reason: str = Reason.GENERIC) -> None:
        """Decline an incoming challenge.

        :param challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        :type reason: :class:`~berserk.enums.Reason`
        """
        path = f"/api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        self._r.post(path, json=payload)


class Board(BaseClient):
    """Client for physical board or external application endpoints."""

    def stream_incoming_events(self) -> Iterator[Dict[str, Any]]:
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        """
        path = "/api/stream/event"
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

        :param time: initial clock time in minutes
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
        path = f"/api/board/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def make_move(self, game_id: str, move: str) -> None:
        """Make a move in a board game.

        :param game_id: ID of a game
        :param move: move to make
        """
        path = f"/api/board/game/{game_id}/move/{move}"
        self._r.post(path)

    def post_message(self, game_id: str, text: str, spectator: bool = False) -> None:
        """Post a message in a board game.

        :param game_id: ID of a game
        :param text: text of the message
        :param spectator: post to spectator room (else player room)
        """
        path = f"/api/board/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        self._r.post(path, json=payload)

    def get_game_chat(self, game_id: str) -> List[Dict[str, str]]:
        """Get the messages posted in the game chat.

        :param str game_id: ID of a game
        :return: list of game chat events
        """
        path = f"/api/board/game/{game_id}/chat"
        return self._r.get(path, fmt=JSON_LIST)

    def abort_game(self, game_id: str) -> None:
        """Abort a board game.

        :param game_id: ID of a game
        """
        path = f"/api/board/game/{game_id}/abort"
        self._r.post(path)

    def resign_game(self, game_id: str) -> None:
        """Resign a board game.

        :param game_id: ID of a game
        """
        path = f"/api/board/game/{game_id}/resign"
        self._r.post(path)

    def handle_draw_offer(self, game_id: str, accept: bool) -> None:
        """Create, accept, or decline a draw offer.

        To offer a draw, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a draw offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have received a
        draw offer.

        Often, it's easier to call :func:`offer_draw`, :func:`accept_draw`, or
        :func:`decline_draw`.

        :param game_id: ID of an in-progress game
        :param accept: whether to accept
        """
        accept_str = "yes" if accept else "no"
        path = f"/api/board/game/{game_id}/draw/{accept_str}"
        self._r.post(path)

    def offer_draw(self, game_id: str) -> None:
        """Offer a draw in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_draw_offer(game_id, True)

    def accept_draw(self, game_id: str) -> None:
        """Accept an already offered draw in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_draw_offer(game_id, True)

    def decline_draw(self, game_id: str) -> None:
        """Decline an already offered draw in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_draw_offer(game_id, False)

    def handle_takeback_offer(self, game_id: str, accept: bool) -> None:
        """Create, accept, or decline a takeback offer.

        To offer a takeback, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a takeback offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have received a
        takeback offer.

        Often, it's easier to call :func:`offer_takeback`, :func:`accept_takeback`, or
        :func:`decline_takeback`.

        :param game_id: ID of an in-progress game
        :param accept: whether to accept
        """
        accept_str = "yes" if accept else "no"
        path = f"/api/board/game/{game_id}/takeback/{accept_str}"
        self._r.post(path)

    def offer_takeback(self, game_id: str) -> None:
        """Offer a takeback in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_takeback_offer(game_id, True)

    def accept_takeback(self, game_id: str) -> None:
        """Accept an already offered takeback in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_takeback_offer(game_id, True)

    def decline_takeback(self, game_id: str) -> None:
        """Decline an already offered takeback in the given game.

        :param game_id: ID of an in-progress game
        """
        self.handle_takeback_offer(game_id, False)

    def claim_victory(self, game_id: str) -> None:
        """Claim victory when the opponent has left the game for a while.

        Generally, this should only be called once the `opponentGone` event
        is received in the board game state stream and the `claimWinInSeconds`
        time has elapsed.

        :param str game_id: ID of an in-progress game
        """
        path = f"/api/board/game/{game_id}/claim-victory/"
        self._r.post(path)

    def go_berserk(self, game_id: str) -> None:
        """Go berserk on an arena tournament game.

        :param str game_id: ID of an in-progress game
        """
        path = f"/api/board/game/{game_id}/berserk"
        self._r.post(path)


class Bots(BaseClient):
    """Client for bot-related endpoints."""

    def stream_incoming_events(self) -> Iterator[Dict[str, Any]]:
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        """
        path = "/api/stream/event"
        yield from self._r.get(path, stream=True)

    def stream_game_state(self, game_id: str) -> Iterator[Dict[str, Any]]:
        """Get the stream of events for a bot game.

        :param game_id: ID of a game
        :return: iterator over game states
        """
        path = f"/api/bot/game/stream/{game_id}"
        yield from self._r.get(path, stream=True, converter=models.GameState.convert)

    def get_online_bots(self, limit: int | None = None) -> Iterator[Dict[str, Any]]:
        """Stream the online bot users.

        :param limit: Maximum number of bot users to fetch
        :return: iterator over online bots
        """
        path = "/api/bot/online"
        params = {"nb": limit}
        yield from self._r.get(
            path, params=params, stream=True, fmt=NDJSON, converter=models.User.convert
        )

    def make_move(self, game_id: str, move: str) -> None:
        """Make a move in a bot game.

        :param game_id: ID of a game
        :param move: move to make
        """
        path = f"/api/bot/game/{game_id}/move/{move}"
        self._r.post(path)

    def post_message(self, game_id: str, text: str, spectator: bool = False):
        """Post a message in a bot game.

        :param game_id: ID of a game
        :param text: text of the message
        :param spectator: post to spectator room (else player room)
        """
        path = f"/api/bot/game/{game_id}/chat"
        room = "spectator" if spectator else "player"
        payload = {"room": room, "text": text}
        self._r.post(path, json=payload)

    def abort_game(self, game_id: str) -> None:
        """Abort a bot game.

        :param game_id: ID of a game
        """
        path = f"/api/bot/game/{game_id}/abort"
        self._r.post(path)

    def resign_game(self, game_id: str) -> None:
        """Resign a bot game.

        :param game_id: ID of a game
        """
        path = f"/api/bot/game/{game_id}/resign"
        self._r.post(path)

    def accept_challenge(self, challenge_id: str) -> None:
        """Accept an incoming challenge.

        :param challenge_id: ID of a challenge
        """
        path = f"/api/challenge/{challenge_id}/accept"
        self._r.post(path)

    def decline_challenge(
        self, challenge_id: str, reason: str = Reason.GENERIC
    ) -> None:
        """Decline an incoming challenge.

        :param challenge_id: ID of a challenge
        :param reason: reason for declining challenge
        :type reason: :class:`~berserk.enums.Reason`
        """
        path = f"/api/challenge/{challenge_id}/decline"
        payload = {"reason": reason}
        self._r.post(path, json=payload)


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

        Results are the players of a tournament with their scores and
        performance in rank order. Note that results for ongoing
        tournaments can be inconsistent due to ranking changes.

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


class Broadcasts(BaseClient):
    """Broadcast of one or more games."""

    def get_official(self, nb: int | None = None) -> Iterator[Dict[str, Any]]:
        """Get the list of incoming, ongoing, and finished official broadcasts. Sorted
        by start date, most recent first.

        :param nb: maximum number of broadcasts to fetch, default is 20
        :return: iterator over broadcast objects
        """
        path = "/api/broadcast"
        params = {"nb": nb}
        yield from self._r.get(path, params=params, stream=True)

    def create(
        self,
        name: str,
        description: str,
        markdown: str | None = None,
        official: bool = False,
    ) -> Dict[str, Any]:
        """Create a new broadcast.

        :param name: name of the broadcast
        :param description: short description
        :param markdown: long description
        :param official: can only be used by Lichess staff accounts
        :return: created tournament info
        """
        path = "/broadcast/new"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get(self, broadcast_id: str, slug: str = "-") -> Dict[str, Any]:
        """Get a broadcast by ID.

        :param broadcast_id: ID of a broadcast
        :param slug: slug for SEO
        :return: broadcast information
        """
        path = f"/broadcast/{slug}/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update(
        self,
        broadcast_id: str,
        name: str,
        description: str,
        markdown: str | None = None,
        official: bool = False,
        slug: str = "-",
    ) -> Dict[str, Any]:
        """Update an existing broadcast by ID.

        .. note::

            Provide all fields. Values in missing fields will be erased.

        :param broadcast_id: ID of a broadcast
        :param name: name of the broadcast
        :param description: short description
        :param markdown: long description
        :param official: can only be used by Lichess staff accounts
        :param slug: slug for SEO
        :return: updated broadcast information
        """
        path = f"/broadcast/{slug}/{broadcast_id}"
        payload = {
            "name": name,
            "description": description,
            "markdown": markdown,
            "official": official,
        }
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def push_pgn_update(self, broadcast_round_id: str, pgn_games: List[str]) -> None:
        """Manually update an existing broadcast by ID.

        :param broadcast_round_id: ID of a broadcast round
        :param pgn_games: one or more games in PGN format
        """
        path = f"/broadcast/round/{broadcast_round_id}/push"
        games = "\n\n".join(g.strip() for g in pgn_games)
        self._r.post(path, data=games)

    def create_round(
        self,
        broadcast_id: str,
        name: str,
        syncUrl: str | None = None,
        startsAt: int | None = None,
    ) -> Dict[str, Any]:
        """Create a new broadcast round to relay external games.

        :param broadcast_id: broadcast tournament ID
        :param name: Name of the broadcast round
        :param syncUrl: URL that Lichess will poll to get updates about the games.
        :param startsAt: Timestamp in milliseconds of broadcast round start
        :return: broadcast round info
        """
        path = f"/broadcast/{broadcast_id}/new"
        payload = {"name": name, "syncUrl": syncUrl, "startsAt": startsAt}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round(self, broadcast_id: str) -> Dict[str, Any]:
        """Get information about a broadcast round.

        :param broadcast_id: broadcast round id (8 characters)
        :return: broadcast round info
        """
        path = f"/broadcast/-/-/{broadcast_id}"
        return self._r.get(path, converter=models.Broadcast.convert)

    def update_round(
        self,
        broadcast_id: str,
        name: str,
        syncUrl: str | None = None,
        startsAt: int | None = None,
    ) -> Dict[str, Any]:
        """Update information about a broadcast round that you created.

        :param broadcast_id: broadcast round id
        :param name: Name of the broadcast round
        :param syncUrl: URL that Lichess will poll to get updates about the games
        :param startsAt: Timestamp in milliseconds of broadcast start
        :return: updated broadcast information
        """
        path = f"/broadcast/round/{broadcast_id}/edit"
        payload = {"name": name, "syncUrl": syncUrl, "startsAt": startsAt}
        return self._r.post(path, json=payload, converter=models.Broadcast.convert)

    def get_round_pgns(self, broadcast_round_id: str) -> Iterator[str]:
        """Get all games of a single round of a broadcast in pgn format.

        :param broadcast_round_id: broadcast round ID
        :return: iterator over all games of the broadcast round in PGN format
        """
        path = f"/api/broadcast/round/{broadcast_round_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)

    def get_pgns(self, broadcast_id: str) -> Iterator[str]:
        """Get all games of all rounds of a broadcast in PGN format.

        :param broadcast_id: the broadcast ID
        :return: iterator over all games of the broadcast in PGN format
        """
        path = f"/api/broadcast/{broadcast_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)


class Simuls(BaseClient):
    """Simultaneous exhibitions - one vs many."""

    def get(self) -> Dict[str, Any]:
        """Get recently finished, ongoing, and upcoming simuls.

        :return: current simuls
        """
        path = "/api/simul"
        return self._r.get(path)


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(self, study_id: str, chapter_id: str) -> str:
        """Export one chapter of a study.

        :return: chapter PGN
        """
        path = f"/api/study/{study_id}/{chapter_id}.pgn"
        return self._r.get(path, fmt=PGN)

    def export(self, study_id: str) -> Iterator[str]:
        """Export all chapters of a study.

        :return: iterator over all chapters as PGN
        """
        path = f"/api/study/{study_id}.pgn"
        yield from self._r.get(path, fmt=PGN, stream=True)


class Messaging(BaseClient):
    def send(self, username: str, text: str) -> None:
        """Send a private message to another player.

        :param username: the user to send the message to
        :param text: the text to send
        """
        path = f"/inbox/{username}"
        payload = {"text": text}
        self._r.post(path, data=payload)


class OAuth(BaseClient):
    def test_tokens(self, *tokens: str) -> Dict[str, Any]:
        """Test the validity of up to 1000 OAuth tokens.

        Valid OAuth tokens will be returned with their
        associated user ID and scopes. Invalid tokens
        will be returned as null.

        :param tokens: one or more OAuth tokens
        :return: info about the tokens
        """
        path = "/api/token/test"
        payload = ",".join(tokens)
        return self._r.post(path, data=payload, converter=models.OAuth.convert)


class Puzzles(BaseClient):
    """Client for puzzle-related endpoints."""

    def get_daily(self) -> Dict[str, Any]:
        """Get the current daily Lichess puzzle.

        :return: current daily puzzle
        """
        path = "api/puzzle/daily"
        return self._r.get(path)

    def get(self, id: str) -> Dict[str, Any]:
        """Get a puzzle by its id.

        :param id: the id of the puzzle to retrieve
        :return: the puzzle
        """
        path = f"/api/puzzle/{id}"
        return self._r.get(path)

    def get_puzzle_activity(
        self, max: int | None = None, before: int | None = None
    ) -> Iterator[Dict[str, Any]]:
        """Stream puzzle activity history of the authenticated user, starting with the most recent activity.

        :param max: maximum number of entries to stream. defaults to all activity
        :param before: timestamp in milliseconds. only stream activity before this time. defaults to now. use together with max for pagination
        :return: iterator over puzzle activity history
        """
        path = "/api/puzzle/activity"
        params = {"max": max, "before": before}
        return self._r.get(
            path,
            params=params,
            fmt=NDJSON,
            stream=True,
            converter=models.PuzzleActivity.convert,
        )

    def get_puzzle_dashboard(self, days: int = 30) -> Dict[str, Any]:
        """Get the puzzle dashboard of the authenticated user.

        :param days: how many days to look back when aggregating puzzle results
        :return: the puzzle dashboard
        """
        path = f"api/puzzle/dashboard/{days}"
        return self._r.get(path)

    def get_storm_dashboard(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get storm dashboard of a player. Set days to 0 if you're only interested in the highscore.

        :param username: the username of the player to download the dashboard for
        :param days: how many days of history to return
        :return: the storm dashboard
        """
        path = f"api/storm/dashboard/{username}"
        params = {"days": days}
        return self._r.get(path, params=params)


class TV(FmtClient):
    """Client for TV related endpoints."""

    def get_current_games(self) -> Dict[str, Any]:
        """Get basic information about the current TV games being played.

        :return: best ongoing games in each speed and variant
        """
        path = "/api/tv/channels"
        return self._r.get(path)

    def stream_current_game(self) -> Iterator[Dict[str, Any]]:
        """Streams the current TV game.

        :return: positions and moves of the current TV game
        """
        path = "/api/tv/feed"
        yield from self._r.get(path, stream=True)

    def get_best_ongoing(
        self,
        channel: str,
        as_pgn: bool | None = None,
        count: int | None = None,
        moves: bool = True,
        pgnInJson: bool = False,
        tags: bool = True,
        clocks: bool = False,
        opening: bool = False,
    ) -> str | List[Dict[str, Any]]:
        """Get a list of ongoing games for a given TV channel in PGN or NDJSON.

        :param channel: the name of the TV channel in camel case
        :param as_pgn: whether to return the game in PGN format
        :param count: the number of games to fetch [1..30]
        :param moves: whether to include the PGN moves
        :param pgnInJson: include the full PGN within JSON response
        :param tags: whether to include the PGN tags
        :param clocks: whether to include clock comments in the PGN moves
        :param opening: whether to include the opening name
        :return: the ongoing games of the given TV channel in PGN or NDJSON
        """
        path = f"/api/tv/{channel}"
        params = {
            "nb": count,
            "moves": moves,
            "pgnInJson": pgnInJson,
            "tags": tags,
            "clocks": clocks,
            "opening": opening,
        }
        if self._use_pgn(as_pgn):
            return self._r.get(path, params=params, fmt=PGN)
        else:
            return self._r.get(
                path, params=params, fmt=NDJSON_LIST, converter=models.TV.convert
            )


class Tablebase(BaseClient):
    """Client for tablebase related endpoints."""

    def look_up(
        self,
        position: str,
        variant: Literal["standard"]
        | Literal["atomic"]
        | Literal["antichess"] = "standard",
    ) -> Dict[str, Any]:
        """Look up the tablebase result for a position.

        :param position: FEN of the position to look up
        :param variant: the variant of the position to look up (supported are standard, atomic, and antichess)
        :return: tablebase information about this position
        """
        path = f"/{variant}"
        params = {"fen": position}
        return self._r.get(path, params=params)

    def standard(self, position: str) -> Dict[str, Any]:
        """Look up the tablebase result for a standard chess position.

        :param position: FEN of the position to lookup
        :return: tablebase information about this position
        """
        return self.look_up(position, "standard")

    def atomic(self, position: str) -> Dict[str, Any]:
        """Look up the tablebase result for an atomic chess position.

        :param position: FEN of the position to lookup
        :return: tablebase information about this position
        """
        return self.look_up(position, "atomic")

    def antichess(self, position: str) -> Dict[str, Any]:
        """Look up the tablebase result for an antichess position.

        :param position: FEN of the position to lookup
        :return: tablebase information about this position
        """
        return self.look_up(position, "antichess")
