# -*- coding: utf-8 -*-
"""Base clients."""
from typing import Optional

import requests

from ..formats import JSON
from ..session import Requestor

API_URL = "https://lichess.org/"


class BaseClient:
    """Base client containing Requestor."""

    def __init__(self, session: requests.Session, base_url: Optional[str] = None):
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
        base_url: Optional[str] = None,
        pgn_as_default: bool = False,
    ):
        super().__init__(session, base_url)
        self.pgn_as_default = pgn_as_default

    def _use_pgn(self, as_pgn: Optional[bool] = None):
        # helper to merge default with provided arg
        return as_pgn if as_pgn is not None else self.pgn_as_default
