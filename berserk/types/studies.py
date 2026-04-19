from __future__ import annotations

from typing_extensions import TypedDict
from typing import Literal, TypeAlias


class ChapterIdName(TypedDict):
    id: str
    name: str

StudyUserSelection: TypeAlias = Literal["nobody", "owner", "contributor", "member", "everyone"]
