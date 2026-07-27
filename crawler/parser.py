from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_page(base_url,html):

    soup = BeautifulSoup(html,"lxml")
    title = soup.title.string.strip() if soup.title else "No title"
    links = []
    for tag in soup.find_all("a",href=True):
        absolute = urljoin(base_url,tag["href"])
        links.append(absolute)
    return title,links