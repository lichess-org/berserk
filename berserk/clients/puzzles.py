from __future__ import annotations

from typing import Iterator, Any, Dict, cast

from .. import models
from ..formats import NDJSON
from .base import BaseClient
from ..types import PuzzleRace


class Puzzles(BaseClient):
    """Client for puzzle-related endpoints."""

    def get_daily(self) -> Dict[str, Any]:
        """Get the current daily Lichess puzzle.

        :return: current daily puzzle
        """
        path = "/api/puzzle/daily"
        return self._r.get(path)

    def get(self, id: str) -> Dict[str, Any]:
        """Get a puzzle by its id.

        :param id: the id of the puzzle to retrieve
        :return: the puzzle
        """
        path = f"/api/puzzle/{id}"
        return self._r.get(path)

    def get_puzzle_activity(
        self, max: int | None = None, before: int | None = None
    ) -> Iterator[Dict[str, Any]]:
        """Stream puzzle activity history of the authenticated user, starting with the
        most recent activity.

        :param max: maximum number of entries to stream. defaults to all activity
        :param before: timestamp in milliseconds. only stream activity before this time.
            defaults to now. use together with max for pagination
        :return: iterator over puzzle activity history
        """
        path = "/api/puzzle/activity"
        params = {"max": max, "before": before}
        yield from self._r.get(
            path,
            params=params,
            fmt=NDJSON,
            stream=True,
            converter=models.PuzzleActivity.convert,
        )

    def get_puzzle_dashboard(self, days: int = 30) -> Dict[str, Any]:
        """Get the puzzle dashboard of the authenticated user.

        :param days: how many days to look back when aggregating puzzle results
        :return: the puzzle dashboard
        """
        path = f"/api/puzzle/dashboard/{days}"
        return self._r.get(path)

    def get_storm_dashboard(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get storm dashboard of a player. Set days to 0 if you're only interested in
        the high score.

        :param username: the username of the player to download the dashboard for
        :param days: how many days of history to return
        :return: the storm dashboard
        """
        path = f"/api/storm/dashboard/{username}"
        params = {"days": days}
        return self._r.get(path, params=params)

    def create_race(self) -> PuzzleRace:
        """Create a new private puzzle race. The Lichess user who creates the race must join the race page,
        and manually start the race when enough players have joined.

        :return: puzzle race ID and URL
        """
        path = "/api/racer"
        return cast(PuzzleRace, self._r.post(path))

    def next(self, angle: str = "mix", difficulty: Any = "normal"):
        """Get a random Lichess puzzle in JSON format. If authenticated,
        only returns puzzles that the user has never seen before.

         :param angle: The theme or opening to filter puzzles with.
         :param difficulty: Enum:"easiest" "easier" "normal" "harder" "hardest"

         :return: the next puzzle"""
        path = "/api/puzzle/next"

        allowed_themes = [
            "advancedPawn",
            "advancedPawnDescription",
            "advantage",
            "advantageDescription",
            "anastasiaMate",
            "anastasiaMateDescription",
            "arabianMate",
            "arabianMateDescription",
            "attackingF2F7",
            "attackingF2F7Description",
            "attraction",
            "attractionDescription",
            "backRankMate",
            "backRankMateDescription",
            "bishopEndgame",
            "bishopEndgameDescription",
            "bodenMate",
            "bodenMateDescription",
            "castling",
            "castlingDescription",
            "capturingDefender",
            "capturingDefenderDescription",
            "crushing",
            "crushingDescription",
            "doubleBishopMate",
            "doubleBishopMateDescription",
            "dovetailMate",
            "dovetailMateDescription",
            "equality",
            "equalityDescription",
            "kingsideAttack",
            "kingsideAttackDescription",
            "clearance",
            "clearanceDescription",
            "defensiveMove",
            "defensiveMoveDescription",
            "deflection",
            "deflectionDescription",
            "discoveredAttack",
            "discoveredAttackDescription",
            "doubleCheck",
            "doubleCheckDescription",
            "endgame",
            "endgameDescription",
            "enPassantDescription",
            "exposedKing",
            "exposedKingDescription",
            "fork",
            "forkDescription",
            "hangingPiece",
            "hangingPieceDescription",
            "hookMate",
            "hookMateDescription",
            "interference",
            "interferenceDescription",
            "intermezzo",
            "intermezzoDescription",
            "knightEndgame",
            "knightEndgameDescription",
            "long",
            "longDescription",
            "master",
            "masterDescription",
            "masterVsMaster",
            "masterVsMasterDescription",
            "mate",
            "mateDescription",
            "mateIn1",
            "mateIn1Description",
            "mateIn2",
            "mateIn2Description",
            "mateIn3",
            "mateIn3Description",
            "mateIn4",
            "mateIn4Description",
            "mateIn5",
            "mateIn5Description",
            "middlegame",
            "middlegameDescription",
            "oneMove",
            "oneMoveDescription",
            "opening",
            "openingDescription",
            "pawnEndgame",
            "pawnEndgameDescription",
            "pin",
            "pinDescription",
            "promotion",
            "promotionDescription",
            "queenEndgame",
            "queenEndgameDescription",
            "queenRookEndgame",
            "queenRookEndgameDescription",
            "queensideAttack",
            "queensideAttackDescription",
            "quietMove",
            "quietMoveDescription",
            "rookEndgame",
            "rookEndgameDescription",
            "sacrifice",
            "sacrificeDescription",
            "short",
            "shortDescription",
            "skewer",
            "skewerDescription",
            "smotheredMate",
            "smotheredMateDescription",
            "superGM",
            "superGMDescription",
            "trappedPiece",
            "trappedPieceDescription",
            "underPromotion",
            "underPromotionDescription",
            "veryLong",
            "veryLongDescription",
            "xRayAttack",
            "xRayAttackDescription",
            "zugzwang",
            "zugzwangDescription",
            "mix",
            "mixDescription",
            "playerGames",
            "playerGamesDescription",
            "puzzleDownloadInformation",
        ]

        allowed_levels = {
            1: "easiest",
            2: "easy",
            3: "normal",
            4: "harder",
            5: "hardest",
        }

        if angle not in allowed_themes:
            raise KeyError("Entered theme not supported")

        if isinstance(difficulty, str):
            difficulty = difficulty.lower()
            if difficulty not in allowed_levels.values():
                raise KeyError(
                    "Please enter a difficulty which is one of "
                    "easiest, easier, normal, harder, hardest"
                    " or corresponding numbers 1, 2, 3, 4, 5"
                )
        elif isinstance(difficulty, int):
            if difficulty < 1 or difficulty > 5:
                raise KeyError(
                    "Please enter a difficulty which is one of "
                    "easiest, easier, normal, harder, hardest"
                    " or corresponding numbers 1, 2, 3, 4, 5"
                )
            difficulty = allowed_levels[difficulty]

        params = {"angle": angle, "difficulty": difficulty}
        return self._r.get(path, params=params)
