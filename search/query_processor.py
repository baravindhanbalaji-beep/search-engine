from indexer.cleaner import TextCleaner
from indexer.tokenizer import Tokenizer
from indexer.stopwords import StopWordRemover
from indexer.stemmer import Stemmer

class QueryProcessor:

    def __init__(self):
        self.cleaner = TextCleaner()
        self.tokenizer = Tokenizer()
        self.stopword = StopWordRemover()
        self.stemmer = Stemmer()

    def process(self,query):
        query = self.cleaner.clean(query)
        tokens = self.tokenizer.tokenize(query)
        tokens = self.stopword.remove(tokens)
        tokens = self.stemmer.stem(tokens)
        return tokens