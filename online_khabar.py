import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
url = 'https://english.onlinekhabar.com/'

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

recent_updates = soup.find_all('div', class_='ok-news-post rtl-post-small')    

articles_url = []

for each_update in recent_updates:
    content = each_update.find('div', class_='ok-post-contents')
    url = content.find('h2').find('a')['href']
    articles_url.append(url)

articles_data = []

for each_article_url in articles_url:
    article_response = requests.get(each_article_url)
    article_soup = BeautifulSoup(article_response.text, features='html.parser')

    title = article_soup.find('div', class_='ok-post-header').find('h1').get_text(strip=True)
    content_paragraphs = article_soup.find('div', class_='post-content-wrap').find_all('p')
    content = '\n'.join(p.get_text(strip=True) for p in content_paragraphs)

    articles_data.append({
        'title': title,
        'content': content,
        'url': each_article_url,
        'scraped_at': datetime.now().isoformat()
    })

print(articles_data)