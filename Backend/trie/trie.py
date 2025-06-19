from utils.logger import setup_logger

logger = setup_logger(__name__)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_query = False

class Trie:
    def __init__(self):
        logger.debug("Initializing Trie...")
        self.root = TrieNode()

    def insert(self, query):
        logger.debug(f"Inserting word: {query}")
        node = self.root
        for char in query:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_query = True
        logger.debug(f"Word '{query}' inserted successfully.")

    def autocomplete(self, prefix):
        logger.debug(f"Searching for prefix: {prefix}")
        node = self.root
        for char in prefix:
            if char not in node.children:
                logger.debug(f"Prefix '{prefix}' not found.")
                return []
            node = node.children[char]
        logger.debug(f"Prefix '{prefix}' found.")
        suggestions = self._find_suggestions(node, prefix)
        valid_suggestions = [s for s in suggestions if s.strip() == s]
        return valid_suggestions[:3]

    def _find_suggestions(self, node, prefix):
        logger.debug(f"Collecting words for prefix: {prefix}")
        suggestions = []
        if node.is_end_of_query:
            suggestions.append(prefix)
        for char, child_node in node.children.items():
            suggestions.extend(self._find_suggestions(child_node, prefix + char))
        return suggestions[:3]

    def get_all_words(self):
        return self._collect_words(self.root, "")

    def _collect_words(self, node, prefix):
        words = []
        if node.is_end_of_query:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._collect_words(child_node, prefix + char))
        return words

    def get_depth_and_width(self):
        def dfs(node, current_depth):
            nonlocal max_depth, max_width
            if node is None:
                return
            max_depth = max(max_depth, current_depth)
            max_width = max(max_width, len(node.children))
            for child in node.children.values():
                dfs(child, current_depth + 1)

        max_depth = 0
        max_width = 0
        dfs(self.root, 0)
        return max_depth, max_width
