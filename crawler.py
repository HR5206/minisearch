import urllib.robotparser
import urllib.parse
import collections
import requests

def crawl(seed_urls, max_depth=2, max_pages=50):
    queue = collections.deque([(url, 0) for url in seed_urls])
    visited = set()
    crawled_data = {}
    rp_cache = {}

    while queue and len(crawled_data) < max_pages:
        url, depth = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        parsed_url = urllib.parse.urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        if base_url not in rp_cache:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(urllib.parse.urljoin(base_url, "/robots.txt"))
            try:
                rp.read()
            except Exception:
                pass
            rp_cache[base_url] = rp
            
        rp = rp_cache[base_url]
        try:
            if not rp.can_fetch("*", url):
                continue
        except Exception:
            pass

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                continue
            html = response.text
        except Exception:
            continue

        links = []
        if depth < max_depth:
            parts = html.split('href="')
            for part in parts[1:]:
                link_end = part.find('"')
                if link_end != -1:
                    raw_link = part[:link_end]
                    full_link = urllib.parse.urljoin(url, raw_link)
                    if full_link.startswith("http"):
                        links.append(full_link)
                        if full_link not in visited:
                            queue.append((full_link, depth + 1))

        crawled_data[url] = {
            "raw_html": html,
            "links": list(set(links))
        }

    return crawled_data
