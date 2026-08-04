import os
from config import PAGE_DIR

os.makedirs(PAGE_DIR,exist_ok=True)

def save_page(page_id,html):
    filename = os.path.join(PAGE_DIR,f"{page_id}.html")
    with open(filename,"w",encoding="utf-8") as file:
        file.write(html)
        return filename