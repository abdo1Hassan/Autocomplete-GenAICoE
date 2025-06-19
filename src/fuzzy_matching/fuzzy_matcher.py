from rapidfuzz.distance import Levenshtein


class FuzzyMatcher:
    def __init__(self, queries):
        self.queries = [tuple(q) for q in queries]

    def match(self, query, max_distance=2):
        matches = []
        for candidate in self.queries:
            if self._is_close_match(query, candidate[0], max_distance):
                matches.append(candidate)

        # Apply minimum length filter on the query string
        matches = [m for m in matches if len(m[0]) >= len(query) * 0.7]
        # Sort by query string length
        matches = sorted(matches, key=lambda m: len(m[0]))[:3]
        return matches

    def _is_close_match(self, query, candidate, max_distance):
        distance = Levenshtein.distance(query, candidate)
        return distance <= max_distance
