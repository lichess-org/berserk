"""Common enumerations"""
from typing_extensions import Final

__all__ = ["PerfType", "Variant", "Color", "Room", "Mode", "Position", "Reason"]


class GameType:
    ANTICHESS = "antichess"
    ATOMIC = "atomic"
    CHESS960 = "chess960"
    CRAZYHOUSE = "crazyhouse"
    HORDE = "horde"
    KING_OF_THE_HILL = "kingOfTheHill"
    RACING_KINGS = "racingKings"
    THREE_CHECK = "threeCheck"


class PerfType(GameType):
    BULLET = "bullet"
    BLITZ = "blitz"
    RAPID = "rapid"
    CLASSICAL = "classical"
    ULTRA_BULLET = "ultraBullet"


class AllPerfType(PerfType):
    """Perfs including puzzles, etc"""

    STORM: str = "storm"
    RACER: str = "racer"
    STREAK: str = "streak"
    PUZZLE: str = "puzzle"


class Variant(GameType):
    STANDARD = "standard"


class Color:
    WHITE = "white"
    BLACK = "black"


class Room:
    PLAYER = "player"
    SPECTATOR = "spectator"


class Mode:
    CASUAL = "casual"
    RATED = "rated"


class Reason:
    GENERIC = "Generic"
    LATER = "later"
    TOOFAST = "tooFast"
    TOOSLOW = "tooSlow"
    TIMECONTROL = "timeControl"
    RATED = "rated"
    CASUAL = "casual"
    STANDARD = "standard"
    VARIANT = "variant"
    NOBOT = "noBot"
    ONLYBOT = "onlyBot"


class CountTypes:
    """Types of games."""

    ALL: Final[str] = "all"
    RATED: Final[str] = "rated"
    AI: Final[str] = "ai"
    DRAW: Final[str] = "draw"
    DRAW_H: Final[str] = "drawH"
    LOSS: Final[str] = "loss"
    LOSS_H: Final[str] = "lossH"
    WIN: Final[str] = "win"
    WIN_H: Final[str] = "winH"
    BOOKMARK: Final[str] = "bookmark"
    PLAYING: Final[str] = "playing"
    IMPORT: Final[str] = "import"
    ME: Final[str] = "me"


class StreamingService:
    """Streaming services."""

    YOUTUBE: Final[str] = "youTube"
    TWITCH: Final[str] = "twitch"


# fmt: off
class Position:
    ALEKHINES_DEFENCE = 'rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2'  # noqa: E501
    ALEKHINES_DEFENCE__MODERN_VARIATION = 'rnbqkb1r/ppp1pppp/3p4/3nP3/3P4/5N2/PPP2PPP/RNBQKB1R b KQkq - 1 4'  # noqa: E501
    BENKO_GAMBIT = 'rnbqkb1r/p2ppppp/5n2/1ppP4/2P5/8/PP2PPPP/RNBQKBNR w KQkq b6 1 4'  # noqa: E501
    BENONI_DEFENCE__CZECH_BENONI = 'rnbqkb1r/pp1p1ppp/5n2/2pPp3/2P5/8/PP2PPPP/RNBQKBNR w KQkq - 0 4'  # noqa: E501
    BENONI_DEFENCE__MODERN_BENONI = 'rnbqkb1r/pp1p1ppp/4pn2/2pP4/2P5/8/PP2PPPP/RNBQKBNR w KQkq - 0 4'  # noqa: E501
    BISHOPS_OPENING = 'rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR b KQkq - 2 2'  # noqa: E501
    BLACKMAR_DIEMER_GAMBIT = 'rnbqkbnr/ppp1pppp/8/3p4/3PP3/8/PPP2PPP/RNBQKBNR b KQkq e3 1 2'  # noqa: E501
    BOGO_INDIAN_DEFENCE = 'rnbqk2r/pppp1ppp/4pn2/8/1bPP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 3 4'  # noqa: E501
    BONGCLOUD_ATTACK = 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR b kq - 0 2'  # noqa: E501
    BUDAPEST_DEFENCE = 'rnbqkb1r/pppp1ppp/5n2/4p3/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3'  # noqa: E501
    CARO_KANN_DEFENCE = 'rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 2'  # noqa: E501
    CARO_KANN_DEFENCE__ADVANCE_VARIATION = 'rnbqkbnr/pp2pppp/2p5/3pP3/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    CARO_KANN_DEFENCE__CLASSICAL_VARIATION = 'rn1qkbnr/pp2pppp/2p5/5b2/3PN3/8/PPP2PPP/R1BQKBNR w KQkq - 2 5'  # noqa: E501
    CARO_KANN_DEFENCE__EXCHANGE_VARIATION = 'rnbqkbnr/pp2pppp/2p5/3P4/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    CARO_KANN_DEFENCE__PANOV_BOTVINNIK_ATTACK = 'rnbqkb1r/pp3ppp/4pn2/3p4/2PP4/2N5/PP3PPP/R1BQKBNR w KQkq - 1 6'  # noqa: E501
    CARO_KANN_DEFENCE__STEINITZ_VARIATION = 'rnbqkb1r/pp3ppp/4pn2/3p4/2PP4/2N5/PP3PPP/R1BQKBNR w KQkq - 1 6'  # noqa: E501
    CATALAN_OPENING = 'rnbqkb1r/pppp1ppp/4pn2/8/2PP4/6P1/PP2PP1P/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    CATALAN_OPENING__CLOSED_VARIATION = 'rnbqk2r/ppp1bppp/4pn2/3p4/2PP4/5NP1/PP2PPBP/RNBQK2R b KQkq - 4 5'  # noqa: E501
    CLOSED_GAME = 'rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2'  # noqa: E501
    DANISH_GAMBIT = 'rnbqkbnr/pppp1ppp/8/8/3pP3/2P5/PP3PPP/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    DUTCH_DEFENCE = 'rnbqkbnr/ppppp1pp/8/5p2/3P4/8/PPP1PPPP/RNBQKBNR w KQkq f6 1 2'  # noqa: E501
    DUTCH_DEFENCE__LENINGRAD_VARIATION = 'rnbqk2r/ppppp1bp/5np1/5p2/2PP4/5NP1/PP2PPBP/RNBQK2R b KQkq - 4 5'  # noqa: E501
    DUTCH_DEFENCE__STAUNTON_GAMBIT = 'rnbqkb1r/ppppp1pp/5n2/6B1/3Pp3/2N5/PPP2PPP/R2QKBNR b KQkq - 4 4'  # noqa: E501
    DUTCH_DEFENCE__STONEWALL_VARIATION = 'rnbq1rk1/ppp1b1pp/4pn2/3p1p2/2PP4/5NP1/PP2PPBP/RNBQ1RK1 w - d6 1 7'  # noqa: E501
    ENGLISH_OPENING = 'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 1 1'  # noqa: E501
    ENGLISH_OPENING__CLOSED_SYSTEM = 'r1bqk1nr/ppp2pbp/2np2p1/4p3/2P5/2NP2P1/PP2PPBP/R1BQK1NR w KQkq - 0 6'  # noqa: E501
    ENGLISH_OPENING__REVERSED_SICILIAN = 'rnbqkbnr/pppp1ppp/8/4p3/2P5/8/PP1PPPPP/RNBQKBNR w KQkq e6 1 2'  # noqa: E501
    ENGLISH_OPENING__SYMMETRICAL_VARIATION = 'rnbqkbnr/pp1ppppp/8/2p5/2P5/8/PP1PPPPP/RNBQKBNR w KQkq c6 1 2'  # noqa: E501
    FOUR_KNIGHTS_GAME = 'r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 5 4'  # noqa: E501
    FOUR_KNIGHTS_GAME__SCOTCH_VARIATION = 'r1bqkb1r/pppp1ppp/2n2n2/4p3/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq d3 1 4'  # noqa: E501
    FOUR_KNIGHTS_GAME__SPANISH_VARIATION = 'r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 0 4'  # noqa: E501
    FRANKENSTEIN_DRACULA_VARIATION = 'rnbqkb1r/pppp1ppp/8/4p3/2B1n3/2N5/PPPP1PPP/R1BQK1NR w KQkq - 0 4'  # noqa: E501
    FRENCH_DEFENCE = 'rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 2'  # noqa: E501
    FRENCH_DEFENCE__ADVANCE_VARIATION = 'rnbqkbnr/ppp2ppp/4p3/3pP3/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    FRENCH_DEFENCE__BURN_VARIATION = 'rnbqkb1r/ppp2ppp/4pn2/3p2B1/3PP3/2N5/PPP2PPP/R2QKBNR b KQkq - 1 4'  # noqa: E501
    FRENCH_DEFENCE__CLASSICAL_VARIATION = 'rnbqkb1r/ppp2ppp/4pn2/3p4/3PP3/2N5/PPP2PPP/R1BQKBNR w KQkq - 3 4'  # noqa: E501
    FRENCH_DEFENCE__EXCHANGE_VARIATION = 'rnbqkbnr/ppp2ppp/4p3/3P4/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    FRENCH_DEFENCE__RUBINSTEIN_VARIATION = 'rnbqkbnr/ppp2ppp/4p3/8/3Pp3/2N5/PPP2PPP/R1BQKBNR w KQkq - 1 4'  # noqa: E501
    FRENCH_DEFENCE__TARRASCH_VARIATION = 'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPPN1PPP/R1BQKBNR b KQkq - 2 3'  # noqa: E501
    FRENCH_DEFENCE__WINAWER_VARIATION = 'rnbqk1nr/ppp2ppp/4p3/3p4/1b1PP3/2N5/PPP2PPP/R1BQKBNR w KQkq - 3 4'  # noqa: E501
    GIUOCO_PIANO = 'r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 5 4'  # noqa: E501
    GRUNFELD_DEFENCE = 'rnbqkb1r/ppp1pp1p/5np1/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq d6 1 4'  # noqa: E501
    GRUNFELD_DEFENCE__BRINCKMANN_ATTACK = 'rnbqkb1r/ppp1pp1p/5np1/3p4/2PP1B2/2N5/PP2PPPP/R2QKBNR b KQkq - 2 4'  # noqa: E501
    GRUNFELD_DEFENCE__EXCHANGE_VARIATION = 'rnbqkb1r/ppp1pp1p/6p1/3n4/3P4/2N5/PP2PPPP/R1BQKBNR w KQkq - 1 5'  # noqa: E501
    GRUNFELD_DEFENCE__RUSSIAN_VARIATION = 'rnbqkb1r/ppp1pp1p/5np1/3p4/2PP4/1QN5/PP2PPPP/R1B1KBNR b KQkq - 0 4'  # noqa: E501
    GRUNFELD_DEFENCE__TAIMANOV_VARIATION = 'rnbqk2r/ppp1ppbp/5np1/3p2B1/2PP4/2N2N2/PP2PPPP/R2QKB1R b KQkq - 0 5'  # noqa: E501
    HALLOWEEN_GAMBIT = 'r1bqkb1r/pppp1ppp/2n2n2/4N3/4P3/2N5/PPPP1PPP/R1BQKB1R b KQkq - 1 4'  # noqa: E501
    HUNGARIAN_OPENING = 'rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR b KQkq - 1 1'  # noqa: E501
    ITALIAN_GAME = 'r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 4 3'  # noqa: E501
    ITALIAN_GAME__EVANS_GAMBIT = 'r1bqk1nr/pppp1ppp/2n5/2b1p3/1PB1P3/5N2/P1PP1PPP/RNBQK2R b KQkq b3 1 4'  # noqa: E501
    ITALIAN_GAME__HUNGARIAN_DEFENCE = 'r1bqk1nr/ppppbppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 5 4'  # noqa: E501
    ITALIAN_GAME__TWO_KNIGHTS_DEFENCE = 'r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 5 4'  # noqa: E501
    KINGS_GAMBIT = 'rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq f3 1 2'  # noqa: E501
    KINGS_GAMBIT_ACCEPTED = 'rnbqkbnr/pppp1ppp/8/8/4Pp2/8/PPPP2PP/RNBQKBNR w KQkq - 1 3'  # noqa: E501
    KINGS_GAMBIT_ACCEPTED__BISHOPS_GAMBIT = 'rnbqkbnr/pppp1ppp/8/8/2B1Pp2/8/PPPP2PP/RNBQK1NR b KQkq - 2 3'  # noqa: E501
    KINGS_GAMBIT_ACCEPTED__CLASSICAL_VARIATION = 'rnbqkbnr/pppp1p1p/8/6p1/4Pp2/5N2/PPPP2PP/RNBQKB1R w KQkq - 0 4'  # noqa: E501
    KINGS_GAMBIT_ACCEPTED__MODERN_DEFENCE = 'rnbqkbnr/ppp2ppp/8/3p4/4Pp2/5N2/PPPP2PP/RNBQKB1R w KQkq d6 1 4'  # noqa: E501
    KINGS_GAMBIT_DECLINED__CLASSICAL_VARIATION = 'rnbqk1nr/pppp1ppp/8/2b1p3/4PP2/8/PPPP2PP/RNBQKBNR w KQkq - 2 3'  # noqa: E501
    KINGS_GAMBIT_DECLINED__FALKBEER_COUNTERGAMBIT = 'rnbqkbnr/ppp2ppp/8/3pp3/4PP2/8/PPPP2PP/RNBQKBNR w KQkq d6 1 3'  # noqa: E501
    KINGS_INDIAN_ATTACK = 'rnbqkbnr/ppp1pppp/8/3p4/8/5NP1/PPPPPP1P/RNBQKB1R b KQkq - 1 2'  # noqa: E501
    KINGS_INDIAN_DEFENCE = 'rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 1 3'  # noqa: E501
    KINGS_INDIAN_DEFENCE__4E4 = 'rnbqk2r/ppp1ppbp/3p1np1/8/2PPP3/2N5/PP3PPP/R1BQKBNR w KQkq - 1 5'  # noqa: E501
    KINGS_INDIAN_DEFENCE__AVERBAKH_VARIATION = 'rnbq1rk1/ppp1ppbp/3p1np1/6B1/2PPP3/2N5/PP2BPPP/R2QK1NR b KQ - 4 6'  # noqa: E501
    KINGS_INDIAN_DEFENCE__CLASSICAL_VARIATION = 'rnbq1rk1/ppp1ppbp/3p1np1/8/2PPP3/2N2N2/PP2BPPP/R1BQK2R b KQ - 4 6'  # noqa: E501
    KINGS_INDIAN_DEFENCE__FIANCHETTO_VARIATION = 'rnbqk2r/ppp1ppbp/3p1np1/8/2PP4/2N2NP1/PP2PP1P/R1BQKB1R b KQkq - 1 5'  # noqa: E501
    KINGS_INDIAN_DEFENCE__FOUR_PAWNS_ATTACK = 'rnbqk2r/ppp1ppbp/3p1np1/8/2PPPP2/2N5/PP4PP/R1BQKBNR b KQkq f3 1 5'  # noqa: E501
    KINGS_INDIAN_DEFENCE__SAMISCH_VARIATION = 'rnbqk2r/ppp1ppbp/3p1np1/8/2PPP3/2N2P2/PP4PP/R1BQKBNR b KQkq - 1 5'  # noqa: E501
    KINGS_PAWN = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 1 1'
    LONDON_SYSTEM = 'rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R b KQkq - 4 3'  # noqa: E501
    MODERN_DEFENCE = 'rnbqkbnr/pppppp1p/6p1/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'  # noqa: E501
    MODERN_DEFENCE__ROBATSCH_DEFENCE = 'rnbqk1nr/ppppppbp/6p1/8/3PP3/2N5/PPP2PPP/R1BQKBNR b KQkq - 0 3'  # noqa: E501
    NIMZO_INDIAN_DEFENCE = 'rnbqk2r/pppp1ppp/4pn2/8/1bPP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 3 4'  # noqa: E501
    NIMZO_INDIAN_DEFENCE__CLASSICAL_VARIATION = 'rnbqk2r/pppp1ppp/4pn2/8/1bPP4/2N5/PPQ1PPPP/R1B1KBNR b KQkq - 4 4'  # noqa: E501
    NIMZO_INDIAN_DEFENCE__FISCHER_VARIATION = 'rnbqk2r/p1pp1ppp/1p2pn2/8/1bPP4/2N1P3/PP3PPP/R1BQKBNR w KQkq - 0 5'  # noqa: E501
    NIMZO_INDIAN_DEFENCE__HUBNER_VARIATION = 'r1bqk2r/pp3ppp/2nppn2/2p5/2PP4/2PBPN2/P4PPP/R1BQK2R w KQkq - 0 8'  # noqa: E501
    NIMZO_INDIAN_DEFENCE__KASPAROV_VARIATION = 'rnbqk2r/pppp1ppp/4pn2/8/1bPP4/2N2N2/PP2PPPP/R1BQKB1R b KQkq - 0 4'  # noqa: E501
    NIMZO_INDIAN_DEFENCE__LENINGRAD_VARIATION = 'rnbqk2r/pppp1ppp/4pn2/6B1/1bPP4/2N5/PP2PPPP/R2QKBNR b KQkq - 0 4'  # noqa: E501
    NIMZO_INDIAN_DEFENCE__SAMISCH_VARIATION = 'rnbqk2r/pppp1ppp/4pn2/8/2PP4/P1P5/4PPPP/R1BQKBNR b KQkq - 0 5'  # noqa: E501
    NIMZO_LARSEN_ATTACK = 'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 1 1'  # noqa: E501
    OLD_INDIAN_DEFENCE = 'rnbqkb1r/ppp1pppp/3p1n2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 1 3'  # noqa: E501
    OPEN_GAME = 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
    PETROVS_DEFENCE = 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 3 3'  # noqa: E501
    PETROVS_DEFENCE__CLASSICAL_ATTACK = 'rnbqkb1r/ppp2ppp/3p4/8/3Pn3/5N2/PPP2PPP/RNBQKB1R b KQkq d3 1 5'  # noqa: E501
    PETROVS_DEFENCE__STEINITZ_ATTACK = 'rnbqkb1r/pppp1ppp/5n2/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq d3 1 3'  # noqa: E501
    PETROVS_DEFENCE__THREE_KNIGHTS_GAME = 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 4 3'  # noqa: E501
    PHILIDOR_DEFENCE = 'rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 3'  # noqa: E501
    PIRC_DEFENCE = 'rnbqkb1r/ppp1pppp/3p1n2/8/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 2 3'  # noqa: E501
    PIRC_DEFENCE__AUSTRIAN_ATTACK = 'rnbqkb1r/ppp1pp1p/3p1np1/8/3PPP2/2N5/PPP3PP/R1BQKBNR b KQkq f3 1 4'  # noqa: E501
    PIRC_DEFENCE__CLASSICAL_VARIATION = 'rnbqkb1r/ppp1pp1p/3p1np1/8/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 2 4'  # noqa: E501
    QUEENS_GAMBIT = 'rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 1 2'  # noqa: E501
    QUEENS_GAMBIT_ACCEPTED = 'rnbqkbnr/ppp1pppp/8/8/2pP4/8/PP2PPPP/RNBQKBNR w KQkq - 1 3'  # noqa: E501
    QUEENS_GAMBIT_DECLINED__ALBIN_COUNTERGAMBIT = 'rnbqkbnr/ppp2ppp/8/3pp3/2PP4/8/PP2PPPP/RNBQKBNR w KQkq e6 1 3'  # noqa: E501
    QUEENS_GAMBIT_DECLINED__CHIGORIN_DEFENCE = 'r1bqkbnr/ppp1pppp/2n5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 2 3'  # noqa: E501
    QUEENS_GAMBIT_DECLINED__SEMI_SLAV_DEFENCE = 'rnbqkb1r/pp3ppp/2p1pn2/3p4/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq - 1 5'  # noqa: E501
    QUEENS_GAMBIT_DECLINED__SEMI_TARRASCH_DEFENCE = 'rnbqkb1r/pp3ppp/4pn2/2pp4/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq c6 1 5'  # noqa: E501
    QUEENS_GAMBIT_DECLINED__SLAV_DEFENCE = 'rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3'  # noqa: E501
    QUEENS_GAMBIT_DECLINED__TARRASCH_DEFENCE = 'rnbqkbnr/pp3ppp/4p3/2pp4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4'  # noqa: E501
    QUEENS_INDIAN_DEFENCE = 'rnbqkb1r/p1pp1ppp/1p2pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 1 4'  # noqa: E501
    QUEENS_PAWN = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 1 1'  # noqa: E501
    QUEENSS_PAWN_GAME__MODERN_DEFENCE = 'rnbqk1nr/ppp1ppbp/3p2p1/8/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 1 4'  # noqa: E501
    RICHTER_VERESOV_ATTACK = 'rnbqkb1r/ppp1pppp/5n2/3p2B1/3P4/2N5/PPP1PPPP/R2QKBNR b KQkq - 4 3'  # noqa: E501
    RUY_LOPEZ = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 4 3'  # noqa: E501
    RUY_LOPEZ__BERLIN_DEFENCE = 'r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 5 4'  # noqa: E501
    RUY_LOPEZ__CLASSICAL_VARIATION = 'r1bqk1nr/pppp1ppp/2n5/1Bb1p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 5 4'  # noqa: E501
    RUY_LOPEZ__CLOSED_VARIATION = 'r1bqk2r/2ppbppp/p1n2n2/1p2p3/4P3/1B3N2/PPPP1PPP/RNBQR1K1 b kq - 0 7'  # noqa: E501
    RUY_LOPEZ__EXCHANGE_VARIATION = 'r1bqkbnr/1ppp1ppp/p1B5/4p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 1 4'  # noqa: E501
    RUY_LOPEZ__MARSHALL_ATTACK = 'r1bq1rk1/2p1bppp/p1n2n2/1p1pp3/4P3/1BP2N2/PP1P1PPP/RNBQR1K1 w - - 0 9'  # noqa: E501
    RUY_LOPEZ__SCHLIEMANN_DEFENCE = 'r1bqkbnr/pppp2pp/2n5/1B2pp2/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq f6 1 4'  # noqa: E501
    RETI_OPENING = 'rnbqkbnr/ppp1pppp/8/3p4/2P5/5N2/PP1PPPPP/RNBQKB1R b KQkq c3 1 2'  # noqa: E501
    SCANDINAVIAN_DEFENCE = 'rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 1 2'  # noqa: E501
    SCANDINAVIAN_DEFENCE__MODERN_VARIATION = 'rnbqkb1r/ppp1pppp/5n2/3P4/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 3'  # noqa: E501
    SCOTCH_GAME = 'r1bqkbnr/pppp1ppp/2n5/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq d3 1 3'  # noqa: E501
    SCOTCH_GAME__CLASSICAL_VARIATION = 'r1bqk1nr/pppp1ppp/2n5/2b5/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 2 5'  # noqa: E501
    SCOTCH_GAME__MIESES_VARIATION = 'r1bqkb1r/p1pp1ppp/2p2n2/4P3/8/8/PPP2PPP/RNBQKB1R b KQkq - 1 6'  # noqa: E501
    SCOTCH_GAME__STEINITZ_VARIATION = 'r1b1kbnr/pppp1ppp/2n5/8/3NP2q/8/PPP2PPP/RNBQKB1R w KQkq - 2 5'  # noqa: E501
    SICILIAN_DEFENCE = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 1 2'  # noqa: E501
    SICILIAN_DEFENCE__ACCELERATED_DRAGON = 'r1bqkbnr/pp1ppp1p/2n3p1/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5'  # noqa: E501
    SICILIAN_DEFENCE__ALAPIN_VARIATION = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/2P5/PP1P1PPP/RNBQKBNR b KQkq - 1 2'  # noqa: E501
    SICILIAN_DEFENCE__CLOSED_VARIATION = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 2 2'  # noqa: E501
    SICILIAN_DEFENCE__DRAGON_VARIATION = 'rnbqkb1r/pp2pp1p/3p1np1/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 1 6'  # noqa: E501
    SICILIAN_DEFENCE__GRAND_PRIX_ATTACK = 'r1bqkbnr/pp1ppppp/2n5/2p5/4PP2/2N5/PPPP2PP/R1BQKBNR b KQkq f3 1 3'  # noqa: E501
    SICILIAN_DEFENCE__HYPER_ACCELERATED_DRAGON = 'rnbqkbnr/pp1ppp1p/6p1/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2'  # noqa: E501
    SICILIAN_DEFENCE__KAN_VARIATION = 'rnbqkbnr/1p1p1ppp/p3p3/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5'  # noqa: E501
    SICILIAN_DEFENCE__NAJDORF_VARIATION = 'rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 1 6'  # noqa: E501
    SICILIAN_DEFENCE__RICHTER_RAUZER_VARIATION = 'r1bqkb1r/pp2pppp/2np1n2/6B1/3NP3/2N5/PPP2PPP/R2QKB1R b KQkq - 5 6'  # noqa: E501
    SICILIAN_DEFENCE__SCHEVENINGEN_VARIATION = 'rnbqkb1r/pp3ppp/3ppn2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 1 6'  # noqa: E501
    SICILIAN_DEFENCE__SMITH_MORRA_GAMBIT = 'rnbqkbnr/pp1ppppp/8/8/3pP3/2P5/PP3PPP/RNBQKBNR b KQkq - 1 3'  # noqa: E501
    SOKOLSKY_OPENING = 'rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b KQkq - 1 1'  # noqa: E501
    TORRE_ATTACK = 'rnbqkb1r/ppp1pppp/5n2/3p2B1/3P4/5N2/PPP1PPPP/RN1QKB1R b KQkq - 4 3'  # noqa: E501
    TROMPOWSKY_ATTACK = 'rnbqkb1r/pppppppp/5n2/6B1/3P4/8/PPP1PPPP/RN1QKBNR b KQkq - 3 2'  # noqa: E501
    VIENNA_GAME = 'rnbqkbnr/pppp1ppp/8/4p3/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 2 2'  # noqa: E501
    ZUKERTORT_OPENING = 'rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1'  # noqa: E501
# fmt: on
