from typing import Optional
from src.trie.trie import Trie
from src.fuzzy_matching.fuzzy_matcher import FuzzyMatcher


class GlobalState:
    """
    Global state for the application.
    """

    _instance = None
    trie: Optional[Trie] = None
    fuzzy_matcher: Optional[FuzzyMatcher] = None

    @classmethod
    def initialize(cls, trie: Trie, fuzzy_matcher: FuzzyMatcher):
        """
        Initializes the global state.
        """
        cls.trie = trie
        cls.fuzzy_matcher = fuzzy_matcher
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance