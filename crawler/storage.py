import os
import json

PAGE_DIR = "data/pages"
os.makedirs(PAGE_DIR,exist_ok=True)

META_DIR = "data/metadata"
os.makedirs(META_DIR,exist_ok=True)
META_FILE = os.path.join(META_DIR,"metadata.json")

def save_page(page_id,html):
    filename = os.path.join(PAGE_DIR,f"{page_id}.html")
    with open(filename,"w",encoding="utf-8") as file:
        file.write(html)

def save_metadata(metadata):
    if os.path.exists(META_FILE):
        try:
            with open(META_FILE,"r",encoding = "utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

    else:
        data = []
    data.append(metadata)
    with open(META_FILE,"w",encoding="utf-8") as file:
        json.dump(data,file,indent=4)