import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
url = "https://www.setopati.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1️ Fetch homepage
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2️ Find article links
article_urls = []
for a in soup.find_all("a", href=True):
    href = a["href"]

    # Only keep Setopati article URLs (pattern: /section/... or /category/...)
    if href.startswith("/"):
        full_url = "https://www.setopati.com" + href
        # Avoid adding non-news pages
        if "/pages/" in full_url or "/privacy-policy" in full_url:
            continue
        if full_url not in article_urls:
            article_urls.append(full_url)

# 3️ Visit each article and extract data
articles_data = []

for article_url in article_urls:
    art_resp = requests.get(article_url, headers=headers)
    art_soup = BeautifulSoup(art_resp.text, "html.parser")

    # Title
    title_tag = art_soup.find("h1")
    if not title_tag:
        continue
    title = title_tag.get_text(strip=True)

    # Content paragraphs
    # Setopati article content is often inside div elements
    content_div = art_soup.find("div")
    paragraphs = content_div.find_all("p") if content_div else []
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    articles_data.append({
        "title": title,
        "content": content,
        "url": article_url,
        "scraped_at": datetime.now().isoformat()
    })

# 4️ Print results
print(articles_data)
