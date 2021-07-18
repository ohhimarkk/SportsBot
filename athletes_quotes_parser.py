from bs4 import BeautifulSoup
import requests
import random
from py3pin.Pinterest import Pinterest
import json


# Этот класс парсит с сайта цитаты спорстменов, а также парсит
# их фотогрфии с помощью Pinterest API.
# Ну, собственно берет рандомную цитату и имя автора, а затем по имени автора
# берет его рандомную фотографию из pinterest
class QuotesParser:

    def __init__(self):
        with open('creds.json', 'r') as f:
            creds = json.load(f)
            f.close()
        # нужно вводить свои данные от аккаунта для подключения к api
        self.pinterest = Pinterest(email=creds['email'],
                                   password=creds['password'],
                                   username=creds['username']
                                   )
        self.pinterest.login()

        # Подключение к сайту с цитатами спорстменов
        self.url = 'https://fydi.ru/55-velikih-tsitat-sportsmenov/'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    # Работа с супом и pinterest api
    def __call__(self):
        quotes = self.soup.find_all('blockquote')
        random_quote = random.choice(quotes)
        author = random_quote.br.next

        search_batch = self.pinterest.search(scope='pins', query=author)
        pin = random.choice(search_batch)
        url = pin['images']['orig']['url']
        img = requests.get(url)
        with open('pin.jpg', 'wb') as f:
            f.write(img.content)
            f.close()
        return random_quote.text
