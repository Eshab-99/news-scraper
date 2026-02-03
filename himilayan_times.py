import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
url = 'https://thehimalayantimes.com/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Fetch homepage
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find article links on homepage
article_links = []

articles = soup.find_all('h3', class_='alith_post_title')

for article in articles:
    a_tag = article.find('a')
    if a_tag and a_tag.get('href'):
        article_links.append(a_tag['href'])

# Visit each article
articles_data = []

for article_url in article_links:
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    # Category / Tag
    tag_mark = article_soup.find('a', class_='alith_post_cat')
    tag = tag_mark.get_text(strip=True) if tag_mark else None

    # Title
    title_tag = article_soup.find('h1', class_='alith_post_title')
    if not title_tag:
        continue
    title = title_tag.get_text(strip=True)

    # Content
    content_section = article_soup.find('div', class_='alith_post_content')
    if not content_section:
        continue

    paragraphs = content_section.find_all('p')
    content = '\n'.join(p.get_text(strip=True) for p in paragraphs)

    articles_data.append({
        'title': title,
        'tag': tag,
        'content': content,
        'url': article_url,
        'scraped_at': datetime.now().isoformat()
    })

print(articles_data)
# File name
file_name = 'himalayan_times.json'
# Write to JSON file
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)
print(f"Data saved to {file_name}")


