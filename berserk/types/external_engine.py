from typing import List

from typing_extensions import TypedDict, NotRequired
from .common import UciVariant


class ExternalEngine(TypedDict):
    # Engine ID
    id: str
    # Engine display name
    name: str
    # Secret token that can be used to request analysis
    clientSecret: str
    # User this engine has been registered for
    userId: str
    # Max number of available threads
    maxThreads: int
    # Max available hash table size, in MiB
    maxHash: int
    # Estimated depth of normal search
    defaultDepth: int
    # List of supported chess variants
    variants: list[UciVariant]
    # Arbitrary data that engine provider can use for identification or bookkeeping
    providerData: NotRequired[str]


class ExternalEngineWork(TypedDict):
    # Arbitrary string that identifies the analysis session. Providers may clear the hash table between sessions
    sessionId: str
    # Number of threads to use for analysis
    threads: int
    # Hash table size to use for analysis, in MiB
    hash: int
    # Requested number of principle variations
    multiPv: List[int]
    # Uci variant
    variant: str
    # Initial position of the game
    initialFen: str
    # List of moves played from the initial position, in UCI notation
    moves: List[str]
    # Request an infinite search (rather than roughly aiming for defaultDepth)
    infinite: NotRequired[bool]


class ExternalEngineRequest(TypedDict):
    id: str
    work: ExternalEngineWork
    engine: ExternalEngine


class PrincipleVariationAnalysis(TypedDict):
    # Current search depth of the pv
    depth: int
    # Variation in UCI notation
    moves: List[str]
    # Evaluation in centi-pawns, from White's point of view
    cp: NotRequired[int]
    # Evaluation in signed moves to mate, from White's point of view
    mate: NotRequired[int]


class EngineAnalysisOutput(TypedDict):
    # Number of milliseconds the search has been going on
    time: int
    # Current search depth
    depth: int
    # Number of nodes visited so far
    nodes: int
    # Information about up to 5 pvs, with the primary pv at index 0
    pvs: List[PrincipleVariationAnalysis]
