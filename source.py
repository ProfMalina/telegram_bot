from short_link import ShortLink
import requests
from bs4 import BeautifulSoup
import feedparser
from db import News
import calendar
import configparser
from db import Database
import logging


class Source(object):
    """ Класс для парсинга RSS-каналов.
    Выделяет из общей информации только интереующие нас поля: Заголовок, ссылку, дату публикации, категорию.
    """
    def __init__(self, config_links):
        config = configparser.ConfigParser()
        config.read('/PATH/TO/BOT/config')
        self.db = Database(config['Database']['Path'])
        self.clck_ru = ShortLink()
        self.links = [config_links[i] for i in config_links]
        self.news = []
        self.white_list_category = ['Общество', 'Мир', 'Страна', 'politics', 'Происшествия', 'Политика',
                                    'Экономическая Политика', 'Экономика', 'economics', 'money', 'finances', 'Деньги',
                                    'Финансы', 'news', 'finance', 'Финансы. Рынок', 'Финансы', 'Занять',
                                    'Инвестировать', 'Бизнес', 'business', 'Недвижимость. Рынок', 'В городе',
                                    'Недвижимость', 'realty', 'own_business', 'Технологии и медиа',
                                    'technology_and_media', 'Hi-Tech', 'technology', 'Стартапы']

    def refresh(self):
        self.refresh_rbc()
        self.refresh_rbc_money()
        self.refresh_vedomosti_news()
        self.refresh_vedomosti_material()
        self.refresh_kommersant_daily()
        self.refresh_kommersant_news()
        self.refresh_kommersant_corp()

    def parse_rbcfreenews(self, url):
        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            try:
                element = soup.find_all('div', 'header__article-category__head')[0].find('span').text.strip()
            except:
                element = soup.find_all('div', 'header__article-category__head')[0].find('span').find('a').text.strip()
        except:
            element = 'rbcfreenews'
        if element == 'Лента новостей':
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            try:
                element = soup.find('title').text.split('::')[1].strip()
            except Exception as err:
                logging.error(err)
                element = 'Лента новостей'
        return element

    def parse_kommers_category(self, i):
        category = ''
        try:  # если в мете все норм
            html = requests.get(i.link).text
            soup = BeautifulSoup(html, 'lxml')
            meta = soup.find(attrs={"name": "mywidget:category"})
            cat = meta['content'].split('.').split(',')
            for i in range(len(cat)):
                if cat[i] in self.white_list_category:
                    category = cat[i]
                    break
            if category == '':  # если cat нет в списке
                try:  # забираем категорию из rss
                    category = i.category
                except:  # если вернулась ошибка, значит i.category нет
                    category = cat[0]
        except:  # если в мете не норм
            try:  # забираем i.category из rss
                if i.category == None:  # если i.category пустая
                    category = 'none'  # берем none так как i.category не приешл
                else:  # иначе забираем из rss
                    category = i.category
            except:  # если вернулась ошибка, то вернем ошибку и запишем ссылки и входящие данные
                category = 'error'
        return category

    def new_rss_row(self, lists):
        new_lists = []
        for i in lists:
            if self.db.find_link(i['link']):
                continue
            else:
                new_lists.append(i)
        return new_lists

    def refresh_rbc(self):
        data = feedparser.parse(self.links[0])
        for_money_rbc = lambda x: 'rbc.ru' if x == 'y.rbc.ru' else 'rbc.ru'
        for_rbcfreenews = lambda x: x.split('/')[3] if x.split('/')[3] != 'rbcfreenews' else self.parse_rbcfreenews(x)
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           for_money_rbc(i['link'].split('/')[2][4:]),
                           for_rbcfreenews(i['link']),
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def refresh_rbc_money(self):
        for_news_in_money = lambda x: 'money' if x == 'news' else x
        data = feedparser.parse(self.links[1])
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           i['link'].split('/')[2][6:],
                           for_news_in_money(i['link'].split('/')[3]),
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def refresh_vedomosti_news(self):
        data = feedparser.parse(self.links[2])
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           i['link'].split('/')[2][4:],
                           i['link'].split('/')[3],
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def refresh_vedomosti_material(self):
        data = feedparser.parse(self.links[3])
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           i['link'].split('/')[2][4:],
                           i['link'].split('/')[3],
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def refresh_kommersant_daily(self):
        data = feedparser.parse(self.links[4])
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           i['link'].split('/')[2][4:],
                           self.parse_kommers_category(i),
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def refresh_kommersant_news(self):
        data = feedparser.parse(self.links[5])
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           i['link'].split('/')[2][4:],
                           self.parse_kommers_category(i),
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def refresh_kommersant_corp(self):
        data = feedparser.parse(self.links[6])
        self.news += [News(i['title'],
                           i['link'],
                           self.clck_ru.short_link(i['link']),
                           i['link'].split('/')[2][4:],
                           self.parse_kommers_category(i),
                           int(calendar.timegm((i['published_parsed'])))) for i in self.new_rss_row(data['entries'])]

    def __repr__(self):
        return "<RSS ('{}','{}')>".format(self.links, len(self.news))
