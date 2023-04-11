# -*- coding: utf-8 -*-
"""Base clients."""
from __future__ import annotations

import requests

from ..formats import JSON
from ..session import Requestor
from .acount import Account
from .games import Games
from .relations import Relations
from .teams import Teams
from .users import Users

__all__ = [
    "Client",
    "Account",
    "Board",
    "Bots",
    "Broadcasts",
    "Challenges",
    "Games",
    "Relations",
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
    """Base client containing Requestor."""

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
