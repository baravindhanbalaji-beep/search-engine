from collections import Counter

class InvertedIndexer:

    def __init__(self,db):
        self.db = db

    def add_document(self,page_id,tokens):
        frequencies = Counter(tokens)
        for token,freq in frequencies.items():
            term_id = self.db.get_or_create_term(token)
            self.db.insert_posting(
                term_id,page_id,freq
            )