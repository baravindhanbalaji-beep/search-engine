class Tokenizer:
    def tokenize(self,text):
        if not text:
            return []
        tokens = text.split()
        return tokens