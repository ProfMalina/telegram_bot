from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, update, and_, Boolean, or_
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

Base = declarative_base()


class User(Base):
    """
    Класс описывающий объект пользователь.Так же, осуществляется взаимодействие с БД.
    Описание полей таблицы ниже.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # Порядковый номер пользователя в телеграм
    first_name = Column(String)  # Имя
    last_name = Column(String)  # Фамилия
    username = Column(String)  # Логин
    name = Column(String)  # title
    stream = Column(Integer)
    rbc = Column(Integer)
    vedomosti = Column(Integer)
    kommersant = Column(Integer)
    politic_view = Column(Integer)
    economy_view = Column(Integer)
    finance_view = Column(Integer)
    business_view = Column(Integer)
    tech_view = Column(Integer)
    acess = Column(Integer)
    flash = Column(Integer)

    def __init__(self, id, first_name, last_name, username, name, stream=0, rbc=1, vedomosti=1, kommersant=1,
                 politic_view=0, economy_view=0, finance_view=0, business_view=0, tech_view=0, acess=0, flash=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.name = name
        self.stream = stream
        self.rbc = rbc
        self.vedomosti = vedomosti
        self.kommersant = kommersant
        self.politic_view = politic_view
        self.economy_view = economy_view
        self.finance_view = finance_view
        self.business_view = business_view
        self.tech_view = tech_view
        self.acess = acess
        self.flash = flash

    def _keys(self):
        return (self.id, self.first_name, self.last_name, self.username, self.name, self.stream,
                self.rbc, self.vedomosti, self.kommersant, self.politic_view, self.economy_view, self.finance_view,
                self.business_view, self.tech_view, self.acess, self.flash)

    def __eq__(self, other):
        return self._keys() == other._keys()

    def __hash__(self):
        return hash(self._keys())

    def __repr__(self):
        return "<User(rbc='{}', vedomosti='{}', kommersant='{}', politic_view='{}', economy_view='{}', " \
               "finance_view='{}', business_view='{}', tech_view='{}', acess='{}', flash='{}')>".format(self.rbc,
                                                                                                    self.vedomosti,
                                                                                                    self.kommersant,
                                                                                                    self.politic_view,
                                                                                                    self.economy_view,
                                                                                                    self.finance_view,
                                                                                                    self.business_view,
                                                                                                    self.tech_view,
                                                                                                    self.acess,
                                                                                                    self.flash)


class News(Base):
    """
    Класс, описывающий объект новости. Так же, осуществляется взаимодействие с БД.
    Описание полей таблицы ниже.
    """
    __tablename__ = 'news'
    id = Column(Integer, autoincrement=True, primary_key=True)  # Порядковый номер новости
    text = Column(String)  # Текст (Заголовок), который будет отправлен в сообщении
    link = Column(String)  # Ссылка на статью на сайте
    short_link = Column(String)  # Короткая ссылка на статью на сайте. Так же отправляется в сообщении
    site = Column(String)  # Сайт с которого новость
    category = Column(String)  # Категория новости
    date = Column(Integer)
    # Дата появления новости на сайте. Носит Чисто информационный характер. UNIX_TIME.
    publish = Column(Integer)
    # Планируемая дата публикации. Сообщение будет отправлено НЕ РАНЬШЕ этой даты. UNIX_TIME.
    chat_id = Column(Integer)
    # Информационный столбец. В данной версии функциональной нагрузки не несет.
    message_id = Column(Integer)

    # Информационный столбец. В данной версии функциональной нагрузки не несет.

    def __init__(self, text, link, short_link, site, category, date, publish=0, chat_id=0, message_id=0):
        self.text = text
        self.link = link
        self.short_link = short_link
        self.site = site
        self.category = category
        self.date = date
        self.publish = publish
        self.chat_id = chat_id
        self.message_id = message_id

    def _keys(self):
        return (self.id, self.text, self.link, self.short_link, self.site)

    def __eq__(self, other):
        return self._keys() == other._keys()

    def __hash__(self):
        return hash(self._keys())

    def __repr__(self):
        return "<News ({}, '{}','{}', '{}', '{}', '{}', {})>".format(self.id,
                                                              self.text,
                                                              self.link,
                                                              self.short_link,
                                                              self.site,
                                                              self.category,
                                                              datetime.fromtimestamp(self.publish))


class Kommers(Base):
    """
    Класс, описывающий объект новости. Так же, осуществляется взаимодействие с БД.
    Описание полей таблицы ниже.
    """
    __tablename__ = 'kommers'
    id = Column(Integer, autoincrement=True, primary_key=True)  # Порядковый номер новости
    text = Column(String)  # Текст (Заголовок), который будет отправлен в сообщении
    link = Column(String)  # Ссылка на статью на сайте
    site = Column(String)  # Сайт с которого новость
    category = Column(String)  # Категория новости
    meta_category = Column(String)  # Категория из тела
    date = Column(Integer)
    # Дата появления новости на сайте. Носит Чисто информационный характер. UNIX_TIME.
    publish = Column(Integer)
    # Планируемая дата публикации. Сообщение будет отправлено НЕ РАНЬШЕ этой даты. UNIX_TIME.

    # Информационный столбец. В данной версии функциональной нагрузки не несет.

    def __init__(self, text, link, site, category, meta_category, date, publish=0):
        self.text = text
        self.link = link
        self.site = site
        self.category = category
        self.meta_category = meta_category
        self.date = date
        self.publish = publish

    def _keys(self):
        return(self.id, self.text, self.link, self.site)

    def __eq__(self, other):
        return self._keys() == other._keys()

    def __hash__(self):
        return hash(self._keys())

    def __repr__(self):
        return "<News ('{}','{}', '{}', '{}', '{}', {})>".format(self.text,
                                                                  self.link,
                                                                  self.site,
                                                                  self.category,
                                                                  self.meta_category,
                                                                  datetime.fromtimestamp(self.publish))


class Database:
    """
    Класс для обработки сессии SQLAlchemy.
    Так же включает в себя минимальный набор методов, вызываемых в управляющем классе.
    Названия методов говорящие.
    """

    def __init__(self, obj):
        engine = create_engine(obj, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_news(self, news):
        self.session.add(news)
        self.session.commit()

    def get_post_without_message_id(self):
        return self.session.query(News).filter(and_(News.message_id == 0,
                                                    News.publish <= int(time.mktime(time.localtime())))).all()

    def update(self, link, chat, msg_id):
        self.session.query(News).filter_by(link=link).update({"chat_id": chat, "message_id": msg_id})
        self.session.commit()

    def find_link(self, link):
        if self.session.query(News).filter_by(link=link).first():
            return True
        else:
            return False

    def find_link_komm(self, link):
        if self.session.query(Kommers).filter_by(link=link).first():
            return True
        else:
            return False

    def add_user(self, usr):
        self.session.add(usr)
        self.session.commit()

    def get_flash(self, user_id, chat_id):
        if self.get_user_from_id(user_id).flash:
            self.session.query(User).filter_by(id=user_id).update({"flash": 0})
            self.session.commit()
            return False
        else:
            self.session.query(User).filter_by(id=user_id).update({"flash": chat_id})
            self.session.commit()
            return True

    def get_add_flash_users(self):
        users = self.session.query(User).filter(User.flash != 0).all()
        return users

    def user(self, user):
        if self.session.query(User).filter_by(id=user.id).first():
            return False
        else:
            usr = User(user['id'],
                       user['first_name'],
                       user['last_name'],
                       user['username'],
                       user['title'])
            self.add_user(usr)
            return True

    def get_user_from_id(self, id_user):
        return self.session.query(User).filter_by(id=id_user).first()

    def get_today_news(self):
        now = list(time.localtime()[3:6])
        today = now[2] + now[1]*60 + now[0]*60*60
        return today

    def get_time_news(self):
        if self.get_today_news() > 2*60*60:
            return int((time.mktime(time.localtime())) - self.get_today_news())
        else:
            return int((time.mktime(time.localtime())) - self.get_today_news() - 3*60*60)

    def get_last_news_id(self):
        return self.session.query(News).filter(News.id).all()[-1].id

    def get_politic(self, user_id):
        news = []
        settings_user = self.get_user_from_id(user_id)
        if settings_user.rbc:
            news_list = self.session.query(News).filter(or_(News.category == 'politics',
                                                            News.category == 'Общество',
                                                            News.category == 'Политика'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'rbc.ru',
                                                            News.id > settings_user.politic_view)
            news.extend(news_list.all())
        if settings_user.kommersant:
            news.extend(self.session.query(News).filter(or_(News.category == 'Мир',
                                                            News.category == 'Общество',
                                                            News.category == 'Страна',
                                                            News.category == 'Происшествия',
                                                            News.category == 'Политика'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'kommersant.ru',
                                                            News.id > settings_user.politic_view).all())
        if settings_user.vedomosti:
            news.extend(self.session.query(News).filter(or_(News.category == 'politics'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'vedomosti.ru',
                                                            News.id > settings_user.politic_view).all())
        return news

    def get_economy(self, user_id):
        news = []
        settings_user = self.get_user_from_id(user_id)
        if settings_user.rbc:
            news.extend(self.session.query(News).filter(or_(News.category == 'economics',
                                                            News.category == 'Экономика'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'rbc.ru',
                                                            News.id > settings_user.economy_view).all())
        if settings_user.kommersant:
            news.extend(self.session.query(News).filter(or_(News.category == 'Экономика',
                                                            News.category == 'Экономическая Политика'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'kommersant.ru',
                                                            News.id > settings_user.economy_view).all())
        if settings_user.vedomosti:
            news.extend(self.session.query(News).filter(or_(News.category == 'economics'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'vedomosti.ru',
                                                            News.id > settings_user.economy_view).all())
        return news

    def get_finance(self, user_id):
        news = []
        settings_user = self.get_user_from_id(user_id)
        if settings_user.rbc:
            news.extend(self.session.query(News).filter(or_(News.category == 'money',
                                                            News.category == 'finances',
                                                            News.category == 'Деньги',
                                                            News.category == 'Финансы'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'rbc.ru',
                                                            News.id > settings_user.finance_view).all())
        if settings_user.vedomosti:
            news.extend(self.session.query(News).filter(or_(News.category == 'finance'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'vedomosti.ru',
                                                            News.id > settings_user.finance_view).all())
        if settings_user.kommersant:
            news.extend(self.session.query(News).filter(or_(News.category == 'Финансы. Рынок',
                                                            News.category == 'Занять',
                                                            News.category == 'Финансы',
                                                            News.category == 'Инвестировать'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'kommersant.ru',
                                                            News.id > settings_user.finance_view).all())
        return news

    def get_business(self, user_id):
        news = []
        settings_user = self.get_user_from_id(user_id)
        if settings_user.rbc:
            news.extend(self.session.query(News).filter(or_(News.category == 'own_business',
                                                            News.category == 'Бизнес',
                                                            News.category == 'business'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'rbc.ru',
                                                            News.id > settings_user.business_view).all())
        if settings_user.kommersant:
            news.extend(self.session.query(News).filter(or_(News.category == 'Бизнес',
                                                            News.category == 'Недвижимость. Рынок',
                                                            News.category == 'В городе',
                                                            News.category == 'Недвижимость'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'kommersant.ru',
                                                            News.id > settings_user.business_view).all())
        if settings_user.vedomosti:
            news.extend(self.session.query(News).filter(or_(News.category == 'business',
                                                            News.category == 'realty'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'vedomosti.ru',
                                                            News.id > settings_user.business_view).all())
        return news

    def get_tech(self, user_id):
        news = []
        settings_user = self.get_user_from_id(user_id)
        if settings_user.rbc:
            news.extend(self.session.query(News).filter(or_(News.category == 'technology_and_media',
                                                            News.category == 'Технологии и медиа'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'rbc.ru',
                                                            News.id > settings_user.tech_view).all())
        if settings_user.kommersant:
            news.extend(self.session.query(News).filter(or_(News.category == 'Hi-Tech',
                                                            News.category == 'Стартапы'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'kommersant.ru',
                                                            News.id > settings_user.tech_view).all())
        if settings_user.vedomosti:
            news.extend(self.session.query(News).filter(or_(News.category == 'technology'),
                                                            News.date >= self.get_time_news(),
                                                            News.site == 'vedomosti.ru',
                                                            News.id > settings_user.tech_view).all())
        return news

    def get_rbc(self, id):
        if self.get_user_from_id(id).rbc:
            self.session.query(User).filter_by(id=id).update({"rbc": 0})
            self.session.commit()
            return True
        else:
            self.session.query(User).filter_by(id=id).update({"rbc": 1})
            self.session.commit()
            return False

    def get_vedomosti(self, id):
        if self.get_user_from_id(id).vedomosti:
            self.session.query(User).filter_by(id=id).update({"vedomosti": 0})
            self.session.commit()
            return True
        else:
            self.session.query(User).filter_by(id=id).update({"vedomosti": 1})
            self.session.commit()
            return False

    def get_kommersant(self, id):
        if self.get_user_from_id(id).kommersant:
            self.session.query(User).filter_by(id=id).update({"kommersant": 0})
            self.session.commit()
            return True
        else:
            self.session.query(User).filter_by(id=id).update({"kommersant": 1})
            self.session.commit()
            return False

    def update_last_view(self, user_id, news_id, rubric):
        self.session.query(User).filter_by(id=user_id).update({rubric: news_id})
        self.session.commit()

    def get_row_for_report(self):
        news = self.session.query(News).filter(News.category != 'Общество')\
                                        .filter( News.category != 'Мир')\
                                        .filter(News.category != 'Страна')\
                                        .filter(News.category != 'politics')\
                                        .filter(News.category != 'Происшествия')\
                                        .filter(News.category != 'Политика')\
                                        .filter(News.category != 'Экономическая Политика')\
                                        .filter(News.category != 'Экономика')\
                                        .filter(News.category != 'economics')\
                                        .filter(News.category != 'money')\
                                        .filter(News.category != 'finances')\
                                        .filter(News.category != 'Деньги')\
                                        .filter(News.category != 'Финансы')\
                                        .filter(News.category != 'news')\
                                        .filter(News.category != 'finance')\
                                        .filter(News.category != 'Финансы. Рынок')\
                                        .filter(News.category != 'Занять')\
                                        .filter(News.category != 'Инвестировать')\
                                        .filter(News.category != 'Бизнес')\
                                        .filter(News.category != 'business')\
                                        .filter(News.category != 'Недвижимость. Рынок')\
                                        .filter(News.category != 'В городе')\
                                        .filter(News.category != 'Недвижимость')\
                                        .filter(News.category != 'realty')\
                                        .filter(News.category != 'own_business')\
                                        .filter(News.category != 'Технологии и медиа')\
                                        .filter(News.category != 'technology_and_media')\
                                        .filter(News.category != 'Hi-Tech')\
                                        .filter(News.category != 'technology')\
                                        .filter(News.category != 'Стартапы')\
                                        .filter(News.date >= int(time.mktime(time.localtime())-24*60*60-5*50)).all()
        return news
