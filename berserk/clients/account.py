from __future__ import annotations

from typing import Any, cast, Dict

from .. import models
from ..types.account import AccountInformation, Preferences
from .base import BaseClient
from ..formats import LIJSON
from ..session import Params


class Account(BaseClient):
    """Client for account-related endpoints."""

    def get(self) -> AccountInformation:
        """Get your public information.

        :return: public information about the authenticated user
        """
        path = "/api/account"
        return cast(
            AccountInformation, self._r.get(path, converter=models.Account.convert)
        )

    def get_email(self) -> str:
        """Get your email address.

        :return: email address of the authenticated user
        """
        path = "/api/account/email"
        return self._r.get(path)["email"]

    def get_preferences(self) -> Preferences:
        """Get your account preferences.

        :return: preferences of the authenticated user
        """
        path = "/api/account/preferences"
        return cast(Preferences, self._r.get(path))

    def get_kid_mode(self) -> bool:
        """Get your kid mode status.

        :return: current kid mode status
        """
        path = "/api/account/kid"
        return self._r.get(path)["kid"]

    def set_kid_mode(self, value: bool) -> None:
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

    def get_timeline(self, since: int = 1356998400070, nb: int = 15) -> Dict[str, Any]:
        """Get your timeline events.

        :param int since: timestamp to show events since, default 1356998400070
        :param int nb: max number of events to fetch, default 15
        :return: timeline events of the authenticated user
        """
        path = "/api/timeline"
        params: Params = {"since": since, "nb": nb}

        return self._r.get(path, fmt=LIJSON, params=params)
