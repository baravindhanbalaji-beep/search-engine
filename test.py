from search.query_processor import QueryProcessor

processor = QueryProcessor()
tokens, phrases = processor.process('"science fiction" books')

print("Tokens:", tokens)
print("Phrases:", phrases)