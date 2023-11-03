from typing import List

from typing_extensions import TypedDict


class PrincipleVariation(TypedDict):
    moves: str
    cp: int
    """Centipawn (cp) is the unit of measure used in chess as representation of the advantage. A centipawn is 1/100th
    of a pawn. This value can be used as an indicator of the quality of play. The fewer centipawns one loses per move,
    the stronger the play.
    """


class PositionEvaluation(TypedDict):
    fen: str
    knodes: int
    depth: int
    pvs: List[PrincipleVariation]
    """Principle Variation (pv) is a variation composed of the "best" moves (in the opinion of the engine)."""
