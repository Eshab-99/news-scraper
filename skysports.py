import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
url = 'https://www.skysports.com/premier-league-news'

# Fetch the page
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all article links
article_tags = soup.find_all('a', href=True)

article_paths = []
for tag in article_tags:
    href = tag['href']
    # Most Sky Sports "news" links include "skysports.com/football/news" pattern
    if "/football/news/" in href:
        full_url = href
        # turn relative into absolute
        if href.startswith("/"):
            full_url = "https://www.skysports.com" + href
        if full_url not in article_paths:
            article_paths.append(full_url)

# Visit articles and extract title & content
articles_data = []

for article_url in article_paths:
    art_resp = requests.get(article_url, headers=headers)
    art_soup = BeautifulSoup(art_resp.text, 'html.parser')

    # Title
    title_tag = art_soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    # Content paragraphs
    paragraphs = art_soup.find_all('p')
    content = '\n'.join(p.get_text(strip=True) for p in paragraphs) if paragraphs else ""

    articles_data.append({
        "title": title,
        "content": content,
        "url": article_url,
        "scraped_at": datetime.now().isoformat()
    })

print(articles_data)
