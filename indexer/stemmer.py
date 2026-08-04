import Stemmer as snowball

class Stemmer:
    def __init__(self):
        self.stemmer = snowball.Stemmer("english")

    def stem(self, tokens):
        return self.stemmer.stemWords(tokens)