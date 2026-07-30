from urllib.parse import urlparse,urlunparse

def same_domain(seed_url, target_url):

    return urlparse(seed_url).netloc == urlparse(target_url).netloc

def url_normalization(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    port = parsed.port
    if (scheme=="http" and port==80) or (scheme=="https" and port==443):
        netloc = hostname
    elif port:
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    path = parsed.path
    if path != "/":
        path = path.rstrip("/")

    return urlunparse((
        scheme,netloc,path,"",parsed.query,""
    ))

