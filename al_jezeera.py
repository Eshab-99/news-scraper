import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import xml.etree.ElementTree as ET

# RSS feed (official)
rss_url = "https://www.aljazeera.com/xml/rss/all.xml"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 1️ Fetch RSS
rss_response = requests.get(rss_url, headers=headers)
root = ET.fromstring(rss_response.content)

# 2️ Get article URLs
article_links = []
for item in root.findall(".//item"):
    link_tag = item.find("link")
    if link_tag is not None:
        article_links.append(link_tag.text)

print(f"Found {len(article_links)} articles in RSS feed.")

# 3️ Visit each article
articles_data = []

for url in article_links:
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title_tag = soup.find("h1")
    if not title_tag:
        continue
    title = title_tag.get_text(strip=True)

    # Content
    content_div = soup.find("div", class_="wysiwyg wysiwyg--all-content")
    paragraphs = content_div.find_all("p") if content_div else []
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    # Optional tag/category
    tag_el = soup.find("a", {"data-element": "article-section"})
    tag = tag_el.get_text(strip=True) if tag_el else None

    articles_data.append({
        "title": title,
        "tag": tag,
        "content": content,
        "url": url,
        "scraped_at": datetime.now().isoformat()
    })

# 4️ Save JSON
file_name = "al_jezeera.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(articles_data)} articles. Data saved to {file_name}")

