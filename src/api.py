from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.trie.trie import Trie
from src.fuzzy_matching.fuzzy_matcher import FuzzyMatcher
from src.utils.file_processor import load_queries
from src.utils.logger import setup_logger

from src.settings import settings
from src.state import GlobalState
from src.dependencies import get_trie, get_fuzzy_matcher

logger = setup_logger(__name__)
app = FastAPI()

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def initialise():
    """
    Initializes the autocomplete system on application startup.
    """
    # === Initialize autocomplete system ===
    queries = load_queries(settings.QUERIES_FILE_PATH)
    trie = Trie()
    fuzzy_matcher = FuzzyMatcher(queries)

    for query in queries:
        trie.insert(query)

    GlobalState.initialize(trie=trie, fuzzy_matcher=fuzzy_matcher)

    # Log trie structure stats
    depth, width = await trie.get_depth_and_width()
    logger.info(f"Trie Stats — Depth: {depth}, Width: {width}")


@app.get("/autocomplete")
async def autocomplete(
    prefix: str = "",
    trie: Trie = Depends(get_trie),
    fuzzy_matcher: FuzzyMatcher = Depends(get_fuzzy_matcher),
):
    try:

        trie_suggestions = await trie.autocomplete(prefix)

        fuzzy_suggestions = []
        if len(trie_suggestions) < settings.MAX_SUGGESTIONS:
            fuzzy_suggestions = fuzzy_matcher.match(prefix)

        suggestions = list(set(trie_suggestions + fuzzy_suggestions))[
            : settings.MAX_SUGGESTIONS
        ]
        print(suggestions)
        return JSONResponse(content={"suggestions": suggestions})

    except Exception as e:
        logger.error(f"Error in autocomplete: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
