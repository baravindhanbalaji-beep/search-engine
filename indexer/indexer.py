from collections import Counter,defaultdict

class InvertedIndexer:

    def __init__(self,db):
        self.db = db

    def add_document(self,page_id,tokens):

        positions = defaultdict(list)

        for position,token in enumerate(tokens):
            positions[token].append(position)

        for token,token_positions in positions.items():
            term_id = self.db.get_or_create_term(token)
            self.db.insert_posting(
                term_id,
                page_id,
                len(token_positions),
                token_positions
            )