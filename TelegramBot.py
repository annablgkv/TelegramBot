import os
import re
import logging
import telebot
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot('287430770:AAHUDybRgVA-2dYCZ07LYhNH8EBf_iOt5dE')
@bot.message_handler(commands=['start'])
def SendInfo(message):
    bot.send_message(message.chat.id, "Привет, я твой бот. Введи запрос для поиска изображений")

@bot.message_handler(commands=['help'])
def SendHelp(message):
    bot.send_message(message.chat.id, "Список доступных команд: /start")
@bot.message_handler(content_types='text')
def SendMessage(message):
    bot.send_message(message.chat.id, "Ожидайте")
    images = SearchGoogleImages(message.text, message.chat.id)
    for image in images:
        bot.send_photo(message.chat.id, open(image, 'rb'))
def SearchGoogleImages(query, id):
    path = os.path.abspath(os.curdir)
    path = os.path.join(path, str(id))

    if not os.path.exists(path):
        os.makedirs(path)

    query = query.split()
    query = '+'.join(query)
    query = 'https://www.google.ru/search?' \
            'q=' + query + \
            '&newwindow=1' \
            '&source=lnms' \
            '&tbm=isch'
    reg = requests.get(query, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/43.0.2357.134 Safari/537.36'})
    soup = bs(reg.content, "html.parser")
    images = soup.find_all('img', {'data-src': re.compile('gstatic.com')})

    imagePaths = []

    for number, tag in enumerate(images[:10]):
        data = requests.get(tag['data-src'])
        image = Image.open(BytesIO(data.content))
        imagePath = os.path.join(path, str(number) + '.' + image.format.lower())
        image.save(imagePath)
        imagePaths.append(imagePath)

    return imagePaths
if __name__ == '__main__':
    logging.basicConfig(filename='botLog.log',
                        format='%(filename)s[LINE:%(lineno)d]# '
                                '%(levelname)-8s [%(asctime)s] '
                                '%(message)s',
                        level=logging.DEBUG)

    logging.info('Start the bot.')

    try:
        bot.polling(none_stop=True)
    except Exception:
        logging.critical('ERROR...')
    finally:
        bot.polling(none_stop=True)




