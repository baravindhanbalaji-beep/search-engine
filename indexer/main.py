import os

from indexer.extractor import TextExtractor
from indexer.cleaner import TextCleaner
from indexer.tokenizer import Tokenizer
from indexer.stopwords import StopWordRemover
from indexer.stemmer import Stemmer
from indexer.indexer import InvertedIndexer
from database.database import DatabaseManager
from config import PAGE_DIR

extractor = TextExtractor()
cleaner = TextCleaner()
tokenizer = Tokenizer()
stopword = StopWordRemover()
stemmer = Stemmer()

db = DatabaseManager()
indexer = InvertedIndexer(db)

pages_indexed = 0

for filename in sorted(os.listdir(PAGE_DIR)):
    if not filename.endswith(".html"):
        continue

    page_id = int(filename.split(".")[0])

    with open(os.path.join(PAGE_DIR, filename), encoding="utf-8") as file:
        html = file.read()

    text = extractor.extract(html)
    text = cleaner.clean(text)

    tokens = tokenizer.tokenize(text)
    tokens = stopword.remove(tokens)
    tokens = stemmer.stem(tokens)

    indexer.add_document(page_id, tokens)

    pages_indexed += 1

db.commit()

print(f"Indexed {pages_indexed} pages")

print(f"Vocabulary Size: {db.get_term_count()}")
print(f"Total Postings : {db.get_posting_count()}")

db.close()