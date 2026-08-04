from collections import defaultdict

class Ranker:

    def __init__(self,db):
        self.db = db

    def rank(self,query_tokens):
        scores = defaultdict(int)

        for token in query_tokens:
            postings = self.db.get_postings(token)

            for page_id,title,url,frequency in postings:
                scores[page_id]+=frequency

        return sorted(
            scores.items(),
            key=lambda x: x[1], reverse=True
        )