from __future__ import annotations

import requests

from .base import BaseClient
from .account import Account
from .users import Users
from .relations import Relations
from .teams import Teams
from .games import Games
from .challenges import Challenges
from .board import Board
from .bots import Bots
from .tournaments import Tournaments
from .broadcasts import Broadcasts
from .simuls import Simuls
from .studies import Studies
from .messaging import Messaging
from .puzzles import Puzzles
from .oauth import OAuth
from .tv import TV
from .tablebase import Tablebase
from .opening_explorer import OpeningExplorer
from .bulk_pairings import BulkPairings
from .external_engine import ExternalEngine

__all__ = [
    "Account",
    "Board",
    "Bots",
    "Broadcasts",
    "BulkPairings",
    "Challenges",
    "Client",
    "ExternalEngine",
    "Games",
    "Messaging",
    "OAuth",
    "Puzzles",
    "Relations",
    "Simuls",
    "Studies",
    "Tablebase",
    "Teams",
    "Tournaments",
    "TV",
    "Users",
]


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
    - :class:`bulk_pairings <berserk.clients.BulkPairing>` - manage bulk pairings
    - :class: `external_engine <berserk.clients.ExternalEngine>` - manage external engines

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
        explorer_url: str | None = None,
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
        self.tablebase = Tablebase(session, tablebase_url)
        self.opening_explorer = OpeningExplorer(session, explorer_url)
        self.bulk_pairings = BulkPairings(session, base_url)
        self.external_engine = ExternalEngine(session, base_url)
