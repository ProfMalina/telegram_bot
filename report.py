from db import Database
import configparser
import time
import smtplib
import xlwt
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


def send_email(rep):

    msg = MIMEMultipart()
    msg['Subject'] = 'Report'
    msg['From'] = 'FROM@EMAIL'
    msg['To'] = ', '.join(["TO@EMAIL"])
    msg.preamble = 'Report\n'
    path=time.strftime("%d %b %Y",time.localtime()) + '.xls'
    attach = MIMEApplication(open(path, 'rb').read())
    attach.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(attach)
    rep = MIMEText(rep)
    msg.attach(rep)

    smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
    smtpObj.starttls()
    smtpObj.login('EMAIL', 'PASSWORD')
    smtpObj.sendmail("FROM@EMAIL", ["TO@EMAIL"],
                     msg.as_string())
    smtpObj.quit()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config')
    db = Database('sqlite:////PATH/TO/DB')
    news = db.get_row_for_report()
    rep = ''

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()

    wb = xlwt.Workbook()
    ws = wb.add_sheet(time.strftime("%d %b %Y", time.localtime()))
    ws.write(0, 0, 'Заголовок', style0)
    ws.write(0, 1, 'Ссылка', style0)
    ws.write(0, 2, 'Сайт', style0)
    ws.write(0, 3, 'Категория', style0)
    ws.write(0, 4, 'Время публикации', style0)

    for n, i in enumerate(news):
        rep += i.text + ' ' + i.link + ' ' + i.site + ' ' + i.category + ' ' + (time.strftime("%H:%M - %d %b %Y",
                                                                                              time.localtime(i.date))
                                                                                + '\n')
        ws.write(n+1, 0, i.text, style1)
        ws.write(n+1, 1, i.link, style1)
        ws.write(n+1, 2, i.site, style1)
        ws.write(n+1, 3, i.category, style1)
        ws.write(n+1, 4, time.strftime("%H:%M - %d %b %Y", time.localtime(i.date)))

    wb.save(time.strftime("%d %b %Y", time.localtime()) + '.xls')
    send_email(rep)
