import requests
import time
from datetime import datetime
from collections import deque
from .config import *
from .parser import parse_page
from .storage import save_page
from .utils import same_domain,url_normalization
import urllib.robotparser
from .logger import logger
from .database import init_database,save_metadata,DB_PATH
import sqlite3

class WebCrawler:
    def __init__(self):
        self.queue = deque()
        self.queue.append((url_normalization(SEED_URL),0))
        self.visited = set()
        self.headers = {
            "User-Agent":USER_AGENT
        }
        self.seen = {SEED_URL}
        robots_url = SEED_URL.rstrip("/"+"/robots.txt")
        self.robot_parser = urllib.robotparser.RobotFileParser()
        self.robot_parser.set_url(robots_url)
        self.robot_parser.read()
        init_database()
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def fetch_page(self,url):
        delay = INITIAL_DELAY
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    url,headers=self.headers,timeout=REQUEST_TIMEOUT
                )

                if response.status_code==200:
                    return response
                logger.warning(
                    f"HTTP {response.status_code} recieved for {url}"
                )

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed:{e}")

            if attempt<MAX_RETRIES-1:
                logger.warning(
                    f"Attemp {attempt+1}/{MAX_RETRIES} failed"
                    f"Retrying in {delay} seconds"
                )
                time.sleep(delay)
                delay*=BACKOFF_FACTOR

        return None
    
    def crawl(self):
        while self.queue and len(self.visited)<MAX_PAGES:
            current_url,depth = self.queue.popleft()
            if depth>MAX_DEPTH:
                continue
            if current_url in self.visited:
                continue
            if not self.robot_parser.can_fetch(USER_AGENT,current_url):
                logger.warning(f"Blocked by robots.txt:{current_url}")
                continue
            response = self.fetch_page(current_url)
            if response is None:
                continue

            self.visited.add(current_url)
            page_id = len(self.visited)
            logger.info(
                f"Page: {page_id} Depth: {depth} URL: {current_url}"
            )

            html_file = save_page(page_id,response.text)
            title,links = parse_page(current_url,response.text)

            save_metadata(
                page_id=page_id,url=current_url,
                title=title,status=response.status_code,
                depth=depth,html_file=html_file,
                timestamp=datetime.now().isoformat()
            )

            logger.info(
                f"Title: {title} Links present: {len(links)}"
            )

            for link in links:
                link = url_normalization(link)
                if(
                    depth<MAX_DEPTH and
                    same_domain(link,SEED_URL) and 
                    link not in self.seen
                ):
                    self.queue.append((link,depth+1))
                    self.seen.add(link)
        logger.info("\nFinished crawling")
        logger.info(f"Pages crawled: {len(self.visited)}")
        self.conn.commit()
        self.conn.close()