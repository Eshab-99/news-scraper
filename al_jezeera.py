import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL – Al Jazeera World News
url = "https://www.aljazeera.com/news/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1️ Fetch homepage
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2️ Find article links
# Articles are in <a> tags with class "fte-featured__link" or "gc__title__link"
article_tags = soup.find_all("a", class_="fte-featured__link") + \
               soup.find_all("a", class_="gc__title__link")

article_urls = []
for tag in article_tags:
    href = tag.get("href")
    if href and href not in article_urls:
        if href.startswith("/"):
            href = "https://www.aljazeera.com" + href
        article_urls.append(href)

# 3️ Visit each article and extract data
articles_data = []

for article_url in article_urls:
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    # Title
    title_tag = article_soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Content
    content_section = article_soup.find("div", class_="wysiwyg wysiwyg--all-content")
    paragraphs = content_section.find_all("p") if content_section else []
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    # Optional: category/tag
    tag_el = article_soup.find("a", {"data-element": "article-section"})
    tag = tag_el.get_text(strip=True) if tag_el else None

    articles_data.append({
        "title": title,
        "tag": tag,
        "content": content,
        "url": article_url,
        "scraped_at": datetime.now().isoformat()
    })

# 4️ Print results
print(articles_data)
