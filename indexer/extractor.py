from bs4 import BeautifulSoup

class TextExtractor:
    def extract(self,html):
        soup = BeautifulSoup(html,"html.parser")

        for tag in soup(["script","style","noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ",strip=True)
        return text