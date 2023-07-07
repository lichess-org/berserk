from __future__ import annotations

from typing import Any, Dict

from .. import models
from .base import BaseClient


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
