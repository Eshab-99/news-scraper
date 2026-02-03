import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import xml.etree.ElementTree as ET

# Target RSS feed
rss_url = "https://www.ratopati.com/feed"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1️ Fetch RSS feed
rss_response = requests.get(rss_url, headers=headers)
rss_content = rss_response.content

# 2️ Parse XML and get article URLs
root = ET.fromstring(rss_content)
article_links = []

for item in root.findall(".//item"):
    link_tag = item.find("link")
    if link_tag is not None:
        article_links.append(link_tag.text)

print(f"Found {len(article_links)} articles in RSS feed.")

# 3️ Visit each article and extract data
articles_data = []

for article_url in article_links:
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    # Title
    title_tag = article_soup.find("h1")
    if not title_tag:
        continue
    title = title_tag.get_text(strip=True)

    # Content (Nepali articles usually in <div class="entry-content">)
    content_div = article_soup.find("div", class_="entry-content")
    if not content_div:
        # fallback: find all <p>
        paragraphs = article_soup.find_all("p")
    else:
        paragraphs = content_div.find_all("p")

    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    # Optional: published date
    date_tag = article_soup.find("time")
    published_date = date_tag.get("datetime") if date_tag else None

    articles_data.append({
        "title": title,
        "content": content,
        "url": article_url,
        "published_date": published_date,
        "scraped_at": datetime.now().isoformat()
    })

# 4️ Save results
file_name = "ratopati.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(articles_data)} articles. Data saved to {file_name}")
