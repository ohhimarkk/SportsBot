from bs4 import BeautifulSoup
import requests
import random
import telebot
import time
import sqlite3


SLEEP_TIME = 20

token = ''
bot = telebot.TeleBot(token, threaded=True)

conn = sqlite3.connect('DataBase/database.db')
cursor = conn.cursor()
# Sql комманда для работы с таблицей
sqlite_select_query = 'SELECT * from user_ids'
cursor.execute(sqlite_select_query)


# Класс, который выделяет рандомную новость с сайта
class RandomNews:

    def __init__(self):
        self.url = 'https://www.pressball.by/news/'

    def __call__(self):
        # Выбираем рандомную из 5-ти послдених страниц на новостном сайте
        page = random.randint(1, 5)
        temp_url = self.url + '?page=' + str(page)

        # Подключаемся
        response = requests.get(temp_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        news_blocks = soup.find_all('table', 'table mb10')
        block = random.randint(1, len(news_blocks) - 1)
        news = news_blocks[block].find_all('a')
        random_news = random.choice(news)

        link = random_news['href']
        inner_resp = requests.get(link)
        inner_soup = BeautifulSoup(inner_resp.content, 'html.parser')
        content = inner_soup.find('div', 'lenta_news')

        # Выделели заголовок новости, перешли по
        # ссылке и взяли сам текст новости,
        # а также ссылку на саму новость и попытались отправить
        try:
            return [random_news.text, link, content.p.text]
        except AttributeError:
            return None


# Цикл, который с интервалом в SLEEP_TIME
# присылает всем пользователям рандомную новость
# вместе с небольшой вырезкой текста из самой новости
while True:
    random_news_auto_post = RandomNews()
    post = random_news_auto_post()
    if post is None:
        continue
    # Обрезаем текст новости до 200 символов с многоточием в конце
    if len(post[2]) > 200:
        post[2] = post[2][:200] + '...'

    # Идем по пользователям имеющимся в БД
    rows = cursor.fetchall()
    for row in rows:
        message = post[0] + '\n\n' + post[2] + '\n' + post[1]
        user_id = row[0]
        # Пытаемся отправить новость, если получаем исключение,
        # значит пользователь отписался от бота
        # и нужно удалить его из БД
        try:
            bot.send_message(user_id, message)
        except telebot.apihelper.ApiException:
            sqlite_delete_query =\
                f'DELETE from user_ids where user_id = {user_id}'
            cursor.execute(sqlite_delete_query)
            conn.commit()

    cursor.execute(sqlite_select_query)
    time.sleep(SLEEP_TIME)
# Точно так же скрипт должен постоянно работать
