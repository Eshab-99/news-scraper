import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL — Ratopati latest news section
url = "https://www.ratopati.com/latest-news"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1️ Fetch the page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2️ Find article links on the page
article_urls = []
for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    # Only include internal Ratopati article links
    if href.startswith("/story/"):
        full_url = "https://www.ratopati.com" + href
        if full_url not in article_urls:
            article_urls.append(full_url)

# 3️ Visit each article and extract data
articles_data = []

for article_url in article_urls:
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    # Title
    title_tag = article_soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Content
    content_section = article_soup.find("div", class_="story-details") 
    paragraphs = content_section.find_all("p") if content_section else []
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    articles_data.append({
        "title": title,
        "content": content,
        "url": article_url,
        "scraped_at": datetime.now().isoformat()
    })

# 4️ Print results
print(articles_data)
