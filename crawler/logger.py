import logging 
import os
from config import LOG_DIR

os.makedirs(LOG_DIR,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(message)s",
    handlers = [
        logging.FileHandler("logs/crawler.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Crawler")