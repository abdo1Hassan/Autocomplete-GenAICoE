from rapidfuzz.distance import Levenshtein


class FuzzyMatcher:
    def __init__(self, queries):
        self.queries = queries

    def match(self, query, max_distance=2):
        matches = []
        for candidate in self.queries:
            if self._is_close_match(query, candidate, max_distance):
                matches.append(candidate)

        # Apply minimum length filter
        matches = [m for m in matches if len(m) >= len(query) * 0.7]
        matches = sorted(matches, key=len)[:3]
        return matches

    def _is_close_match(self, query, candidate, max_distance):
        distance = Levenshtein.distance(query, candidate)
        return distance <= max_distance
