#!/usr/bin/python3
# -*-coding:utf8-*-

from db import Database
import configparser
import logging, logging.config, logging.handlers
import time
import locale
from source import Source

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

config = configparser.ConfigParser()
config.read('/PATH/TO/CONFIG/config')
db = Database('sqlite:////PATH/TO/DB.sqlite')
logging.config.fileConfig('/PATH/TO/log_crawler.conf')
logging.getLogger('main')


def main():
    src = Source(config['RSS'])
    src.refresh()
    news = src.news
    news.reverse()
    # Проверяем на наличие в базе ссылки на новость, если нет, то добавляем в базу данных
    for i in news:
        if not db.find_link(i.link):
            i.id = db.get_last_news_id() + 1
            i.publish = int(time.mktime(time.localtime()))  # видимо cтоит удалить
            logging.info("Detect news: {}".format(i))
            db.add_news(i)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
