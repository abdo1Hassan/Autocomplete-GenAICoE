from src.state import GlobalState
from src.trie.trie import Trie
from src.fuzzy_matching.fuzzy_matcher import FuzzyMatcher


async def get_trie():
    state = GlobalState.get_instance()
    return state.trie


async def get_fuzzy_matcher():
    state = GlobalState.get_instance()
    return state.fuzzy_matcher
