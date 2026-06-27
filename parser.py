from bs4 import BeautifulSoup
import re

def parse(crawled_data):
    parsed_data = {}
    for url, data in crawled_data.items():
        html = data["raw_html"]
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=" ")
        text = re.sub(r'\s+', ' ', text).strip()
        parsed_data[url] = {
            "title": title,
            "text": text,
            "links": data["links"]
        }
    return parsed_data
