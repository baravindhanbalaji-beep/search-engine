import math
from collections import defaultdict

from search.phrase import PhraseMatcher


class Ranker:

    def __init__(self, db):
        self.db = db
        self.phrase_matcher = PhraseMatcher(db)

    def rank(self, query_tokens, phrases=None):

        if phrases is None:
            phrases = []

        N = self.db.get_total_documents()
        scores = defaultdict(float)

        # Normal TF-IDF ranking
        for token in query_tokens:

            df = self.db.get_document_frequency(token)

            if df == 0:
                continue

            idf = math.log((N + 1) / (df + 1)) + 1

            postings = self.db.get_postings(token)

            for page_id, title, url, frequency, positions in postings:
                scores[page_id] += frequency * idf

        # Phrase boost
        for phrase in phrases:

            matching_pages = self.phrase_matcher.match(phrase)

            for page_id in matching_pages:
                scores[page_id] += 5

        return sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )