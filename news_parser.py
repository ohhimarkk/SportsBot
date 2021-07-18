from bs4 import BeautifulSoup
import requests


# Парсит последние главные новости со спортивного сайта
# и возврщает заголовки новостей и ссылки на них
class LastNewsParser:

    def __init__(self):
        self.url = 'https://www.pressball.by/news/'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def __call__(self):
        top_news = self.soup.find('div', 'lenta_top_news')
        return [(news.text, news['href']) for news in top_news.find_all('a')]
