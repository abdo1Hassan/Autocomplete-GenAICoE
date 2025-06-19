from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from time import perf_counter
import uvicorn

from trie.trie import Trie
from fuzzy_matching.fuzzy_matcher import FuzzyMatcher
from embeddings.embedding_model import EmbeddingModel
from utils.file_processor import load_queries
from utils.logger import setup_logger

logger = setup_logger(__name__)
app = FastAPI()

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Initialize autocomplete system ===
queries = load_queries('data/merged_queries_with_tag_cleaned.csv')
trie = Trie()
fuzzy_matcher = FuzzyMatcher(queries)
embedding_model = EmbeddingModel()  # Not used here, but initialized

for query in queries:
    trie.insert(query)

# Log trie structure stats
depth, width = trie.get_depth_and_width()
logger.info(f"📏 Trie Stats — Depth: {depth}, Width: {width}")

@app.post("/autocomplete")
async def autocomplete(request: Request):
    try:
        data = await request.json()
        prefix = data.get('prefix', '')

        start_time = perf_counter()

        trie_suggestions = trie.autocomplete(prefix)
        source = "trie"

        fuzzy_suggestions = []
        if len(trie_suggestions) < 3:
            fuzzy_suggestions = fuzzy_matcher.match(prefix)
            source = "fuzzy" if not trie_suggestions else "mixed"

        suggestions = list(set(trie_suggestions + fuzzy_suggestions))[:3]
        latency = round((perf_counter() - start_time) * 1000, 2)

        # Optional: log latency
        with open("latency_log.csv", "a") as f:
            f.write(f"{prefix},{latency},{source}\n")

        return JSONResponse(content={
            "suggestions": suggestions,
            "latency": latency,
            "source": source
        })

    except Exception as e:
        logger.error(f"Error in autocomplete: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
