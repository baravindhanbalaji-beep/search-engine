from search.query_processor import QueryProcessor
from search.ranker import Ranker

class SearchEngine:

    def __init__(self,db):
        self.db = db
        self.query_processor = QueryProcessor()
        self.ranker = Ranker(db)

    def search(self,query):
        query_tokens = self.query_processor.process(query)

        if not query_tokens:
            return []
        
        ranked_pages = self.ranker.rank(query_tokens)

        results = []

        for page_id,score in ranked_pages:
            title,url = self.db.get_page(page_id)

            results.append({
                "page_id":page_id,"title":title,
                "url":url,"score":score
            })

        return results