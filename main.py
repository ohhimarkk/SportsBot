import telebot
import sqlite3
from telebot import types
from news_parser import LastNewsParser
from upcoming_games_parser import UpcomingGamesParser
from time import sleep
from athletes_quotes_parser import QuotesParser

# Подключаю бота
token = '1718863223:AAEHyeVrBqoAemDoU34HslIDu-hPcVdY2ZM'
bot = telebot.TeleBot(token, threaded=True, num_threads=5)

# Подключаю sqlite базу, в которой храню пользователей бота
conn = sqlite3.connect('DataBase/database.db', check_same_thread=False)
cursor = conn.cursor()


# Обработчик команд
@bot.message_handler(
    commands=['start', 'hot_news', 'upcoming_games', 'tiktok_sport_video'])
def command_processing(message):
    if message.text == '/hot_news':
        send_last_news(message)
    elif message.text == '/start':
        start_answer(message.from_user.id, message.from_user.username)
    elif message.text == '/upcoming_games':
        sport_choice_answer(message.from_user.id)
    elif message.text == '/tiktok_sport_video':
        tiktok_video_answer(message.from_user.id)


# Парсер цитат и функция ответа на каждое сообщение
# цитатой спортсмена с фотографией
quotes_parser = QuotesParser()


@bot.message_handler(func=lambda message: True)
def quote_auto_answer(message):
    text = quotes_parser()
    bot.send_photo(message.from_user.id, open('pin.jpg', 'rb'), text)


# Функция выводит клавиатуру пользователю в ответ на определенный запрос
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    text1 = ''
    callback_data1 = ''
    text2 = ''
    callback_data2 = ''
    text3 = ''
    callback_data3 = ''
    if call.data == 'foot':
        text1 = 'Лига Чемпионов'
        callback_data1 = 'ucl'
        text2 = 'Ла Лига'
        callback_data2 = 'll'
        text3 = 'РФПЛ'
        callback_data3 = 'rfpl'
    elif call.data == 'bask':
        text1 = 'НБА'
        callback_data1 = 'nba'
        text2 = 'Университетская лига NCAA'
        callback_data2 = 'ncaa'
        text3 = 'Единая лига ВТБ'
        callback_data3 = 'vtb'
    elif call.data == 'hock':
        text1 = 'КХЛ'
        callback_data1 = 'chl'
        text2 = 'Национальная ХЛ'
        callback_data2 = 'nhl'
        text3 = 'Американская ХЛ'
        callback_data3 = 'ahl'
    else:
        upcoming_games_parser = UpcomingGamesParser()
        upcoming_games_parser(call.data)
        bot.send_photo(call.message.chat.id,
                       photo=open('screenshot.png', 'rb'),
                       caption='Матчи')
        return
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(
        text=text1,
        callback_data=callback_data1)
    keyboard.add(key1)
    key2 = types.InlineKeyboardButton(
        text=text2,
        callback_data=callback_data2)
    keyboard.add(key2)
    key3 = types.InlineKeyboardButton(
        text=text3,
        callback_data=callback_data3)
    keyboard.add(key3)

    bot.send_message(call.message.chat.id,
                     'Выберите интересующую лигу:',
                     reply_markup=keyboard)


# Начало общения с юзером и добавление его в базу данных
def start_answer(user_id: int, user_name: str):
    bot.send_message(
        user_id,
        '✌️Я помогу вам следить за новостями в мире спорта и не только!')
    add_user_to_db(user_id, user_name)


# Ответ на запрос по выбору спортивной игры с последующим выводом клавиатуры
def sport_choice_answer(user_id):
    keyboard = types.InlineKeyboardMarkup()

    key_football = types.InlineKeyboardButton(
        text='Футбол', callback_data='foot')
    keyboard.add(key_football)
    key_basketball = types.InlineKeyboardButton(
        text='Баскетбол', callback_data='bask')
    keyboard.add(key_basketball)
    key_hockey = types.InlineKeyboardButton(
        text='Хоккей', callback_data='hock')
    keyboard.add(key_hockey)

    bot.send_message(
        user_id,
        text="Выберите интересущий вид спорта:",
        reply_markup=keyboard)


# Функция добавляет пользователя в файл,
# из которого скрипт tiktok.py берет его id и
# прислает рандомный спор(тивный тик ток.
# Да, это жуткий костыль, но по неизвестным мне
# причинам pyTelegramBotApi не захотел
# дружить с TikTokApi и все ломалось, когда они работали
# вместе(что-то там с потоком проблемы у них были)
def tiktok_video_answer(user_id):
    with open('id.txt', 'a') as f:
        f.write(str(user_id) + '\n')
        f.close()


# Добавление юзера в БД
def add_user_to_db(user_id: int, user_name: str):
    cursor.execute(
        'INSERT INTO user_ids (user_id, user_name) VALUES (?, ?)',
        (user_id, user_name))
    conn.commit()


# Вызывает парсер, который возвращает последние
# главные спортивные новости с сайта pressball.by
# и шлет новости пользователю, когда тот вызывает
# соответсвующую команду
def send_last_news(message):
    last_top_news = ''
    last_news_parser = LastNewsParser()
    for news in last_news_parser():
        last_top_news += news[0] + '\n         ' + news[1] + '\n\n'
    bot.send_message(
        message.from_user.id,
        'Последние новости спорта на данный момент:\n\n' + last_top_news)


# Оказалось, что telebot не оч хорошо
# доработан и частенько вылетает,
# поэтому здесь бот реанимируется
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print('Что-то пошло не так у бота, cейчас перезапустим')
        sleep(5)
