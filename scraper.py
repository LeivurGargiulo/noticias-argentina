import requests
from bs4 import BeautifulSoup

def get_latest_news():
    url = "https://www.argentina.gob.ar/noticias"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select(".views-row .noticia-titulo a")
    news = []
    for article in articles:
        title = article.get_text(strip=True)
        link = "https://www.argentina.gob.ar" + article['href']
        news.append((title, link))
    return news
