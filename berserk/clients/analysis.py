from __future__ import annotations

from typing import cast

from ..types import VariantKey
from .base import BaseClient
from ..types.analysis import PositionEvaluation


class Analysis(BaseClient):
    """Client for analysis-related endpoints."""

    def get_cloud_evaluation(
        self,
        fen: str,
        num_variations: int = 1,
        variant: VariantKey = "standard",
    ) -> PositionEvaluation:
        """Get the cached evaluation of a position, if available.

        Opening positions have more chances of being available. There are about 15 million positions in the database.
        Up to 5 variations may be available. Variants are supported.

        :param fen: FEN of a position
        :param num_variations: number of variations
        :param variant: game variant to use
        :return: cloud evaluation of a position
        """
        path = "/api/cloud-eval"
        params = {"fen": fen, "multiPv": num_variations, "variant": variant}
        return cast(PositionEvaluation, self._r.get(path=path, params=params))
