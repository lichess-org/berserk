"""Account client."""
from __future__ import annotations

from deprecated.sphinx import deprecated, versionchanged
from typing_extensions import cast

from .. import models
from ..types.account import AccountInformation, Preferences
from .base import BaseClient


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

    @versionchanged(
        ":py:meth:`berserk.clients.Account.get_preferences` now returns "
        "all the preferences including language",
        version="0.12.8",
    )
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

    @deprecated("Use endpoint from the Bot client instead", version="0.12.8")
    def upgrade_to_bot(self):
        """Upgrade your account to a bot account.

        Requires bot:play oauth scope. User cannot have any previously played games.
        """
        path = "/api/bot/account/upgrade"
        self._r.post(path)
