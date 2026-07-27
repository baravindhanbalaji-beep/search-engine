from urllib.parse import urlparse

def same_domain(seed_url, target_url):

    return urlparse(seed_url).netloc == urlparse(target_url).netloc