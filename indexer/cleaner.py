import re

class TextCleaner:
    def clean(self,text):
        text = text.lower()
        text = text.replace("â", "")
        text = re.sub(r"[^\w\s]"," ",text)
        text = re.sub(r"\s+"," ",text)
        text = text.strip()

        return text