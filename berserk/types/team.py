from __future__ import annotations

from typing import Literal
from typing_extensions import TypedDict, NotRequired

Title = Literal[
    "GM", "WGM", "IM", "WIM", "FM", "WFM", "NM", "CM", "WCM", "WNM", "LM", "BOT"
]


class Team(TypedDict):
    # The id of the team
    id: str
    # The name of the team
    name: str
    # The description of the team
    description: str
    # Whether the team is open
    open: bool
    # The leader of the team
    leader: LightUser
    # The leaders of the team
    leaders: list[LightUser]
    # The number of members of the team
    nbMembers: int
    # Has the user asssociated with the token (if any) joined the team
    joined: bool
    # Has the user asssociated with the token (if any) requested to join the team
    requested: bool


class LightUser(TypedDict):
    # The id of the user
    id: str
    # The name of the user
    name: str
    # The title of the user
    title: NotRequired[Title]
    # The patron of the user
    patron: bool
