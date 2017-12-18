#!/usr/bin/python3
# -*-coding:utf8-*-

import logging.config
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import telegram
from db import Database
import configparser
import time
import smtplib
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

config = configparser.ConfigParser()
config.read('/PATH/TO/BOT/config')
db = Database(config['Database']['Path'])
logging.config.fileConfig('/PATH/TO/BOT/log_bot.conf')
log = logging.getLogger(__name__)

FEEDBACK, FLASH, OFFER, POLITIC, ECONOMY, FINANCE, BUSINESS, TECH = range(8)

# Все конопки
# start
politic_button = telegram.KeyboardButton(text="Политика")
economy_button = telegram.KeyboardButton(text="Экономика")
finance_button = telegram.KeyboardButton(text="Финансы")
business_button = telegram.KeyboardButton(text="Бизнес")
tech_button = telegram.KeyboardButton(text="Технологии и медиа")
option_button = telegram.KeyboardButton(text='Настройки')
# option
source_button = telegram.KeyboardButton(text="Источники")
rubric_button = telegram.KeyboardButton(text="Рубрики")
about_button = telegram.KeyboardButton(text="О нас")
# source
rbc_button = telegram.KeyboardButton(text="РБК")
vedomosti_button = telegram.KeyboardButton(text="Ведомости")
kommersant_button = telegram.KeyboardButton(text="Коммерсант")
flash_button = telegram.KeyboardButton(text="⚡")
offer_button = telegram.KeyboardButton(text="Предложить свой")
# about us
write_to_us_button = telegram.KeyboardButton(text="Написать нам")
feedback_button = telegram.KeyboardButton(text="Оставить отзыв")
# cansel, back, more
back_button = telegram.KeyboardButton(text="Назад")
cansel_button = telegram.KeyboardButton(text="Отмена")
more_button = telegram.KeyboardButton(text="Ещё")


# Все клавиатуры
# start
start_keyboard = [[politic_button, economy_button], [finance_button, business_button], [tech_button, option_button]]
start_markup = telegram.ReplyKeyboardMarkup(start_keyboard)
# option
option_keyboard = [[source_button, about_button], [back_button]]
option_markup = telegram.ReplyKeyboardMarkup(option_keyboard)
# source
source_keyboard = [[rbc_button, vedomosti_button], [kommersant_button, flash_button], [offer_button, back_button]]
source_markup = telegram.ReplyKeyboardMarkup(source_keyboard)
# about
about_keyboard = [[write_to_us_button], [back_button]]
about_markup = telegram.ReplyKeyboardMarkup(about_keyboard)
# back
back_keyboard = [[back_button]]
back_markup = telegram.ReplyKeyboardMarkup(back_keyboard)
# more
more_keyboard = [[more_button, back_button]]
more_markup = telegram.ReplyKeyboardMarkup(more_keyboard, resize_keyboard=True)
# hide
hide_markup = telegram.ReplyKeyboardHide()


# запросы в бд
def rbc(bot, update):
    if db.get_rbc(update.message.chat.id):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='РБК выключен',
                        reply_markup=source_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='РБК включен',
                        reply_markup=source_markup)


def flash(bot, update):
    if db.get_flash(update.message.chat.id, update.message.chat_id):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Режим ⚡ включен\nЭто возможность получать особо-важные новости без запроса, по решению '
                             'редакции и вне зависимости от ваших предпочтений. Мы обещаем не беспокоить вас по '
                             'пустякам, но информировать, только если произойдет что-то экстраординарное',
                        reply_markup=source_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Режим ⚡ выключен',
                        reply_markup=source_markup)


def vedomosti(bot, update):
    if db.get_vedomosti(update.message.chat.id):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='“Ведомости” выключены',
                        reply_markup=source_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='“Ведомости” включены',
                        reply_markup=source_markup)


def kommersant(bot, update):
    if db.get_kommersant(update.message.chat.id):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='“Коммерсант” выключен',
                        reply_markup=source_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='“Коммерсант” включен',
                        reply_markup=source_markup)


def start(bot, update):
    if db.user(update.message.chat):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Больше вам незачем тратить время на поиск деловых новостей на сайтах различных изданий. '
                             'Мы доставляем новости по вашему требованию, в удобное для вас время, по интересным для '
                             'вас темам. Выберите одну из пяти рубрик: Политика, Экономика, Бизнес, Финансы или IT и '
                             'получите новости РБК, «Ведомостей» и «Коммерсанта» с момента вашего последнего обращения '
                             'к боту. Не тратьте время на поиск, читайте заголовки и только те статьи, которые вам '
                             'интересны',
                        reply_markup=start_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Добро пожаловать",
                        reply_markup=start_markup)


def prompt(prompt):
    return input(prompt).strip()


def send_email(user, text, subj):
    smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
    smtpObj.starttls()
    smtpObj.login('E@MA.IL', 'PASSWORD')
    fromaddr = str(user.id) + ' ' + str(user.first_name) + ' ' + str(user.last_name) + ' ' + str(user.username) + ' ' \
               + str(user.title)
    msg = '{}\n{}\n{}'.format(fromaddr, subj, text)
    msg = msg.encode("utf8")
    smtpObj.sendmail("FROM@EMAIL", "TO@EMAIL", msg)
    smtpObj.quit()


def get_smile(site):
    if site == 'rbc.ru':
        return '🇵'
    if site == 'kommersant.ru':
        return '🇰'
    if site == 'vedomosti.ru':
        return '🇧'


def get_msg(bot, update, news, rubric, finish=5):
    news.sort(key=(lambda obj: obj.id))
    if len(news) <= 5:
        for post in news[:len(news)]:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='<i>{3}</i>\n {1} {2} <a href="{0}">{0}</a>'.format(post.short_link,
                                                                                     get_smile(post.site),
                                                                                     post.text,
                                                                                     time.strftime("%H:%M - %d %b %Y",
                                                                                                   time.localtime(
                                                                                                       post.date))),
                            parse_mode=telegram.ParseMode.HTML,
                            disable_web_page_preview=True,
                            reply_markup=hide_markup)
        db.update_last_view(update.message.chat.id, news[len(news)-1].id, rubric)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Других новостей по этой теме пока нет.',
                        reply_markup=start_markup)
        return ConversationHandler.END
    for post in news[:4]:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='<i>{3}</i>\n {1} {2} <a href="{0}">{0}</a>'.format(post.short_link,
                                                                                 get_smile(post.site),
                                                                                 post.text,
                                                                                 time.strftime("%H:%M - %d %b %Y",
                                                                                               time.localtime(
                                                                                                   post.date))),
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True,
                        reply_markup=hide_markup)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='<i>{3}</i>\n {1} {2} <a href="{0}">{0}</a>'.format(news[4].short_link,
                                                                             get_smile(news[4].site),
                                                                             news[4].text,
                                                                             time.strftime("%H:%M - %d %b %Y",
                                                                                           time.localtime(
                                                                                               news[4].date))),
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=more_markup)
    db.update_last_view(update.message.chat.id, news[finish-1].id, rubric)


def politic(bot, update):
    rubric = 'politic_view'
    news = db.get_politic(update.message.chat.id)
    if len(news) == 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Ничего нового пока не случилось.',
                        reply_markup=start_markup)
        return ConversationHandler.END
    if update.message.text == 'Ещё':
        if len(news) > 5:
            get_msg(bot, update, news, rubric)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
            return ConversationHandler.END
        if 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
            return ConversationHandler.END
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=start_markup)
        return ConversationHandler.END


def economy(bot, update):
    rubric = 'economy_view'
    news = db.get_economy(update.message.chat.id)
    if len(news) == 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Ничего нового пока не случилось.',
                        reply_markup=start_markup)
        return ConversationHandler.END
    if update.message.text == 'Ещё':
        if len(news) > 5:
            get_msg(bot, update, news, rubric)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
            return ConversationHandler.END
        if 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
            return ConversationHandler.END
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=start_markup)
        return ConversationHandler.END


def finance(bot, update):
    rubric = 'finance_view'
    news = db.get_finance(update.message.chat.id)
    if len(news) == 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Ничего нового пока не случилось.',
                        reply_markup=start_markup)
        return ConversationHandler.END
    if update.message.text == 'Ещё':
        if len(news) > 5:
            get_msg(bot, update, news, rubric)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
            return ConversationHandler.END
        if 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
            return ConversationHandler.END
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=start_markup)
        return ConversationHandler.END


def business(bot, update):
    rubric = 'business_view'
    news = db.get_business(update.message.chat.id)
    if len(news) == 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Ничего нового пока не случилось.',
                        reply_markup=start_markup)
        return ConversationHandler.END
    if update.message.text == 'Ещё':
        if len(news) > 5:
            get_msg(bot, update, news, rubric)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
            return ConversationHandler.END
        if 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
            return ConversationHandler.END
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=start_markup)
        return ConversationHandler.END


def tech(bot, update):
    rubric = 'tech_view'
    news = db.get_tech(update.message.chat.id)
    if len(news) == 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Ничего нового пока не случилось.',
                        reply_markup=start_markup)
        return ConversationHandler.END
    if update.message.text == 'Ещё':
        if len(news) > 5:
            get_msg(bot, update, news, rubric)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
            return ConversationHandler.END
        if 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
            return ConversationHandler.END
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=start_markup)
        return ConversationHandler.END


def submenu(bot, update):
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=about_markup)
        return ConversationHandler.END
    send_email(update.message.chat, update.message.text, 'feedback')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Спасибо за ваш отзыв',
                    reply_markup=about_markup)
    return ConversationHandler.END


def offer(bot, update):
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=source_markup)
        return ConversationHandler.END
    send_email(update.message.chat, update.message.text, 'offer')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Спасибо за ваше предложение',
                    reply_markup=source_markup)
    return ConversationHandler.END


def menu(bot, update):
    if update.message.text == 'Настройки':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Сделайте выбор',
                        reply_markup=option_markup)
    if update.message.text == 'Политика':
        rubric = 'politic_view'
        news = db.get_politic(update.message.chat.id)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
        elif 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
        elif len(news) > 5:
            get_msg(bot, update, news, rubric)
            return POLITIC
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Ничего нового пока не случилось.',
                            reply_markup=start_markup)
    if update.message.text == 'Экономика':
        rubric = 'economy_view'
        news = db.get_economy(update.message.chat.id)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
        elif 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
        elif len(news) > 5:
            get_msg(bot, update, news, rubric)
            return ECONOMY
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Ничего нового пока не случилось.',
                            reply_markup=start_markup)
    if update.message.text == 'Финансы':
        rubric = 'finance_view'
        news = db.get_finance(update.message.chat.id)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
        elif 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
        elif len(news) > 5:
            get_msg(bot, update, news, rubric)
            return FINANCE
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Ничего нового пока не случилось.',
                            reply_markup=start_markup)
    if update.message.text == 'Бизнес':
        rubric = 'business_view'
        news = db.get_business(update.message.chat.id)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
        elif 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
        elif len(news) > 5:
            get_msg(bot, update, news, rubric)
            return BUSINESS
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Ничего нового пока не случилось.',
                            reply_markup=start_markup)
    if update.message.text == 'Технологии и медиа':
        rubric = 'tech_view'
        news = db.get_tech(update.message.chat.id)
        if len(news) == 5:
            get_msg(bot, update, news, rubric)
        elif 0 < len(news) < 5:
            get_msg(bot, update, news, rubric, len(news))
        elif len(news) > 5:
            get_msg(bot, update, news, rubric)
            return TECH
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Ничего нового пока не случилось.',
                            reply_markup=start_markup)
    if update.message.text == 'Источники':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Вы можете отключить источники и включить их вновь',
                        reply_markup=source_markup)
    if update.message.text == 'РБК':
        rbc(bot, update)
    if update.message.text == 'Ведомости':
        vedomosti(bot, update)
    if update.message.text == 'Коммерсант':
        kommersant(bot, update)
    if update.message.text == '⚡':
        flash(bot, update)
    if update.message.text == 'Предложить свой':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Отправьте сообщение',
                        reply_markup=back_markup)
        return OFFER
    if update.message.text == 'О нас':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Больше вам незачем тратить время на поиск деловых новостей на сайтах различных изданий. '
                             'Мы доставляем новости по вашему требованию, в удобное для вас время, по интересным для '
                             'вас темам. Выберите одну из пяти рубрик: Политика, Экономика, Бизнес, Финансы или IT и '
                             'получите новости РБК, «Ведомостей» и «Коммерсанта» с момента вашего последнего обращения '
                             'к боту. Не тратьте время на поиск, читайте заголовки и только те статьи, которые вам '
                             'интересны',
                        reply_markup=about_markup)
    if update.message.text == 'Написать нам':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Отправьте сообщение',
                        reply_markup=back_markup)
        return FEEDBACK
    if update.message.text == 'Молния':
        if db.get_user_from_id(update.message.chat.id).acess:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Отправьте сообщение или /cancel',
                            reply_markup=start_markup)
            return FLASH
    if update.message.text == 'Назад':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=start_markup)
    if update.message.text == 'Отмена':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Что будем делать?',
                        reply_markup=option_markup)


def cancel(bot, update):
    user = update.message.from_user
    log.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text('Отмена',
                              reply_markup=source_markup)
    return ConversationHandler.END


def hide(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm back.", reply_markup=hide_markup)


def do_flash(bot, update):
    try:
        send_flash(bot, update, update.message.text)
        update.message.reply_text('Отправлено')
    except Exception as err:
        logging.error(err)
        update.message.reply_text('ошибка')
    return ConversationHandler.END


def send_flash(bot, update, text):
    users = db.get_add_flash_users()
    msg = ''
    for user in users:
        try:
            bot.sendMessage(chat_id=user.flash, text='⚡ '+text, disable_web_page_preview=True, reply_markup=start_markup)
        except:
            msg = str(user.flash) + ' ' + user.first_name + ' ' + user.last_name + ' ' + user.username + '\n'
            continue
    if msg != '':
        log.error(msg)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Извините, но такой команды нет.", reply_markup=start_markup)


def main():
    updater = Updater(token=config['Telegram']['access_token'])

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, menu)],

        states={
            FEEDBACK: [MessageHandler(Filters.text, submenu)],
            FLASH:  [MessageHandler(Filters.text, do_flash)],
            OFFER: [MessageHandler(Filters.text, offer)],
            POLITIC: [MessageHandler(Filters.text, politic)],
            ECONOMY: [MessageHandler(Filters.text, economy)],
            FINANCE: [MessageHandler(Filters.text, finance)],
            BUSINESS: [MessageHandler(Filters.text, business)],
            TECH: [MessageHandler(Filters.text, tech)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    keyboard_handler = CommandHandler('start', start)
    dp.add_handler(keyboard_handler)

    menu_handler = MessageHandler(Filters.text, menu)
    dp.add_handler(menu_handler)

    hide_handler = CommandHandler('hide', hide)
    dp.add_handler(hide_handler)

    cancel_handler = CommandHandler('cancel', cancel)
    dp.add_handler(cancel_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log.critical(e)

