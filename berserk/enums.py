__all__ = ["Room", "Mode"]


class GameType:
    ANTICHESS = "antichess"
    ATOMIC = "atomic"
    CHESS960 = "chess960"
    CRAZYHOUSE = "crazyhouse"
    HORDE = "horde"
    KING_OF_THE_HILL = "kingOfTheHill"
    RACING_KINGS = "racingKings"
    THREE_CHECK = "threeCheck"


class Room:
    PLAYER = "player"
    SPECTATOR = "spectator"


class Mode:
    CASUAL = "casual"
    RATED = "rated"
