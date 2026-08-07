class PhraseMatcher:

    def __init__(self, db):
        self.db = db

    def match(self, phrase_tokens):

        if not phrase_tokens:
            return set()

        first_postings = self.db.get_postings_with_positions(
            phrase_tokens[0]
        )

        matches = {
            page_id: set(positions)
            for page_id, positions in first_postings
        }

        for offset, token in enumerate(phrase_tokens[1:], start=1):

            postings = self.db.get_postings_with_positions(token)

            positions_by_page = {
                page_id: set(positions)
                for page_id, positions in postings
            }

            for page_id in list(matches):

                if page_id not in positions_by_page:
                    del matches[page_id]
                    continue

                valid_positions = {
                    position
                    for position in matches[page_id]
                    if position + offset in positions_by_page[page_id]
                }

                if not valid_positions:
                    del matches[page_id]
                else:
                    matches[page_id] = valid_positions

        return set(matches.keys())