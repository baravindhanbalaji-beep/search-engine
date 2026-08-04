class StopWordRemover:
    STOP_WORDS = {
        "a", "an", "the",
        "and", "or", "but",
        "is", "are", "was", "were",
        "am", "be", "been", "being",
        "of", "to", "in", "on", "at",
        "for", "from", "by", "with",
        "as", "that", "this", "these", "those",
        "it", "its", "if", "then", "than",
        "into", "about", "after", "before",
        "over", "under", "between",
        "he", "she", "they", "we", "you", "i"
    }

    def remove(self,tokens):
        return [
            token 
            for token in tokens
            if token not in self.STOP_WORDS
        ]