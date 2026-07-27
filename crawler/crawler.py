import requests
from collections import deque
from .config import *
from .parser import parse_page
from .storage import save_page
from .utils import same_domain

class WebCrawler:
    def __init__(self):
        self.queue = deque()
        self.queue.append(SEED_URL)
        self.visited = set()
        self.headers = {
            "User-Agent":USER_AGENT
        }

    def crawl(self):
        while self.queue and len(self.visited)<MAX_PAGES:
            current_url = self.queue.popleft()
            if current_url in self.visited:
                continue
            print("-"*60)
            print("Visiting: ",current_url)

            try:
                response = requests.get(
                    current_url,headers = self.headers,timeout=REQUEST_TIMEOUT
                )
            except Exception as e:
                print("Failed: ",e)
                continue
            if response.status_code!=200:
                continue
            self.visited.add(current_url)
            save_page(len(self.visited),response.text)
            title,links = parse_page(current_url,response.text)
            print("Title: ",title)
            print("Links found: ",len(links))
            for link in links:
                if same_domain(SEED_URL,link):
                    if link not in self.visited:
                        self.queue.append(link)
        print("\nFinished crawling")
        print("Pages crawled: ",len(self.visited))