from search.search_engine import SearchEngine
from database.database import DatabaseManager

db = DatabaseManager()
engine = SearchEngine(db)

while True:
    query = input("\nSearch > ")
    if query.lower()=="exit":
        break

    results = engine.search(query)
    if not results:
        print("No results found")
        continue

    for result in results:
        print(f"Score : {result['score']}")
        print(f"Title : {result['title']}")
        print(f"URL   : {result['url']}")
        print()