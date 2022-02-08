from TikTokApi import TikTokApi
from random import randint
import telebot
from time import sleep

# Бот
token = ''
bot = telebot.TeleBot(token, threaded=True)


# Класс берет аккаунт в тиктоке и сохраняет
# рандомное видео из аккаунта локально в проект
# и затем отправляет пользователю
class TikTokParser:

    def __init__(self, user_idd):
        self.api = TikTokApi.get_instance(generate_static_did=True)
        self.user = 'sportmomentss33'
        self.user_id = 0
        self.user_id = user_idd

    def __call__(self):
        account_videos = self.api.by_username(username=self.user)
        random_video_num = randint(0, len(account_videos) - 1)
        tiktok_video = self.api.get_video_by_tiktok(
            data=account_videos[random_video_num])
        with open('video.mp4', 'wb') as f:
            f.write(tiktok_video)
        with open('video.mp4', 'rb') as f:
            bot.send_video(self.user_id, f, timeout=500)


# Костыль, который в случае, если есть юзеры, которым
# нужно отправить тикток видео
# вызывает парсер, который это делает.
# Опять-таки жуткий костыль но, подругому было никак
while True:
    users = open('id.txt', 'r+')
    for user in users:
        while True:
            # На всякий случай через try
            try:
                tiktok_parser = TikTokParser(user)
                tiktok_parser()
                break
            except Exception:
                continue

    users.truncate(0)
    users.close()
    sleep(3)
# Этот скрипт также должен запускаться и работать все время,
# чтобы отвечать своевременно на запросы
