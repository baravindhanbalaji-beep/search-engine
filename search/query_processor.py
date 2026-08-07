from indexer.cleaner import TextCleaner
from indexer.tokenizer import Tokenizer
from indexer.stopwords import StopWordRemover
from indexer.stemmer import Stemmer

import re

class QueryProcessor:

    def __init__(self):
        self.cleaner = TextCleaner()
        self.tokenizer = Tokenizer()
        self.stopword = StopWordRemover()
        self.stemmer = Stemmer()

    def process(self,query):
        phrases = re.findall(r'"([^"]+)"',query)
        remaining = re.sub(r'"[^"]+"', '', query)

        remaining = self.cleaner.clean(remaining)
        tokens = self.tokenizer.tokenize(remaining)
        tokens = self.stopword.remove(tokens)
        tokens = self.stemmer.stem(tokens)

        phrase_tokens = []

        for phrase in phrases:
            phrase = self.cleaner.clean(phrase)
            tokens_in_phrase = self.tokenizer.tokenize(phrase)
            tokens_in_phrase = self.stopword.remove(tokens_in_phrase)
            tokens_in_phrase = self.stemmer.stem(tokens_in_phrase)

            phrase_tokens.append(tokens_in_phrase)

        return tokens,phrase_tokens