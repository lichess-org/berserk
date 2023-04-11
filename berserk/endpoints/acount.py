# -*- coding: utf-8 -*-
"""Account-related endpoints."""
from typing import Any, Dict

from .. import models
from . import BaseClient


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
