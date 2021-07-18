from selenium import webdriver
from PIL import Image


# Класс, который получает код запроса,
# на который ему нужно отправить пользователю
# расписание ближайших матчей по игре и лиге,
# которые выбрал пользователей с помощью клавиатуры
class UpcomingGamesParser:

    def __init__(self):
        # Словарь  код: ссылка
        self.urls = {
            "ucl": "https://www.flashscore.ru/football/europe/champions-league/fixtures/",
            "ll": "https://www.flashscore.ru/football/spain/laliga/fixtures/",
            "rfpl": "https://www.flashscore.ru/football/russia/premier-league/fixtures/",
            "nba": "https://www.flashscore.ru/basketball/usa/nba/fixtures/",
            "ncaa": "https://www.flashscore.ru/basketball/usa/ncaa/fixtures/",
            "vtb": "https://www.flashscore.ru/basketball/russia/vtb-united-league/fixtures/",
            "chl": "https://www.flashscore.ru/khl/fixtures/",
            "nhl": "https://www.flashscore.ru/hockey/usa/nhl/fixtures/",
            "ahl": "https://www.flashscore.ru/hockey/usa/ahl/fixtures/"
        }

    # Делает скриншот нужной страницы сайта,
    # обрезает и отправляет пользователю
    def __call__(self, league):
        driver = webdriver.Chrome('chromedriver')
        driver.get(self.urls[league])
        driver.save_screenshot("screenshot.png")
        img = Image.open("screenshot.png")
        crop = img.crop((158, 291, 907, 585))
        crop.save('screenshot.png')
        driver.quit()
