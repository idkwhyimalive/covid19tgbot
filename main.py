#!/usr/bin/python
# -*- coding: utf-8 -*-

# Telegram Bot COVID-19
# Libs: telebot, pandas, requests, bs4, googletranslate
# Присутнє 3 мовних інтерфейси (російська вимкнена, але функціонал присутній)
# Закінчив розробку приблизно 06.07.2020 (15 років) 
# Спочатку використовував базу даних із csv-файлів від coronavirus.jhu.edu, надалі замінив на парсинг даних із сайту worldometers.com/coronavirus. 
# Працює не бездоганно, оскільки це тг-бот, то воно не відображає дані в лайф-таймі, а з затримкою приблизно 30 хв, як я пам'ятаю
# Як я вважаю, в коді присутня досить милиць виходячи з віку, думаю зрозуміло

import telebot
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googletrans import *

trans1=()
trans2=()
trans3=()
translator1 = Translator()
translator2 = Translator()
translator3 = Translator()
TGBot = ''
bot = telebot.TeleBot(TGBot)
keyboard_lang=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_lang.row("English 🇺🇸", "Russian 🇷🇺", "Ukrainian 🇺🇦")

#keyboard_ru=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#keyboard_ru.row("все числа📊", "по стране📌", "смена языка🌍")

keyboard_ua=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_ua.row("всі числа📊", "по країні📌", "зміна мови🌍")

keyboard_en=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_en.row("all numbers📊", "by country📌", "switch language🌎")
next1_message = False
next2_message = False
next3_message = False
flag = 0

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Greetings. To continue working with the bot, select the language on the keyboard below", reply_markup=keyboard_lang)

@bot.message_handler(commands=['language'])
def language_message(message):
    bot.send_message(message.chat.id, "Greetings. To continue working with the bot, select the language on the keyboard below", reply_markup=keyboard_lang)

@bot.message_handler(commands=['infoen'])
def infoen_message(message):
    bot.send_message(message.chat.id, """
    Hey. I am a COVID-19 bot. I’ll tell you about the amounts of coronavirus infected. \n\
Below is a keyboard where you can select a specific option. \n\
For example:
"All numbers📊" - will write the number of infected, dead and recovered, the most relevant number
\n\
"By Country📌" - write data for a specific country written, you can write in any language, the main name of the country.
\n\
By typing / you can get to the menu. Available commands: \n\
    /language - if you want to change the language
    /infoen - This message will be resent \n\n\
Any questions or suggestions?
You can write here -> @idkwhyimalive""", reply_markup=keyboard_en)

#@bot.message_handler(commands=['inforu'])
#def inforu_message(message):           
    #bot.send_message(message.chat.id, """
    #Привет. Я бот COVID-19. Расскажу о количествах зараженных коронавирусом.\n\
#Ниже есть клавиатура где ты можешь выбрать определенную опцию.\n\
#К примеру: 
#"Все числа📊" - напишет количество зараженных, умерших и выздоровевших, самое актуальное число 
#\n\
#"По стране📌" - напишет данные по определенной написанной стране, можно писать на любом языке, главное название страны.
#\n\
#Набрав / можно попасть в меню. Доступные команды: \n\
#    /language - Если вы хотите изменить язык 
#    /inforu - Это сообщение будет отправлено повторно \n\n\
#Есть вопросы или предложения?
#Можете написать сюда -> @idkwhyimalive""", reply_markup=keyboard_ru)
  
@bot.message_handler(commands=['infoua'])
def infoua_message(message):
    bot.send_message(message.chat.id, """
    Вітаю. Я бот COVID-19. Розповім про кількості заражених коронавірусом.\n\
Нижче є клавіатура де ти можеш вибрати певну опцію.\n\
Наприклад:
"Всі числа📊" - напише кількість заражених, померлих і видужавших, найактуальніше число
\n\
"По країні📌" - напише дані по певній написаної країні, можна писати на будь-якій мові, головне назву країни.
\n\
Набравши / можна потрапити в меню. Доступні команди:\n\
    /language - Якщо ви хочете змінити мову
    /infoua - Це повідомлення буде відправлено повторно\n\n\
Є питання або пропозиції?
Можете написати сюди -> @idkwhyimalive""", reply_markup=keyboard_ua)


# Парс для витягування даних зі сторінки з даними про заражених та інше
res = requests.get('https://www.worldometers.info/coronavirus/').text
soup = BeautifulSoup(res,'html.parser')

# Заражені, видужалі, померлі та активні випадки захворювання на коронавірус
cases = soup.findAll("div", {"class": "maincounter-number"})
active = soup.find("div", {"class": "number-table-main"}).get_text().strip()

# Парс, який дістає з сайту час і дату останнього оновлення даних, прибираючи зайве й отримуючи дані у форматі: July 05, 2020, 20:45 GMT
online = soup.findAll("div", {"style": "font-size:13px; color:#999; margin-top:5px; text-align:center"})
online = str(online).replace("""[<div style="font-size:13px; color:#999; margin-top:5px; text-align:center">""","")
online = str(online).replace("</div>]", "")
date = str(online).replace("Last updated: ", "")

@bot.message_handler(content_types=['text'])
def send_message(message):
    global next1_message
    global next2_message
    global next3_message
    global flag
    #Английский интерфейс
    if message.text.lower() == "english 🇺🇸":
        bot.send_message(message.chat.id, "To find out what the bot and its commands can do, type /infoen")
    elif message.text.lower() == "switch language🌎":
        bot.send_message(message.chat.id, "Greetings. To continue working with the bot, select the language on the keyboard below", reply_markup=keyboard_lang)
    elif message.text.lower() == "all numbers📊":
        bot.send_message(message.chat.id,"🦠 Total infected - " + cases[0].text.strip() + "\n" + "⚰ Deaths - " + cases[1].text.strip() + "\n" + "👥 Recovered - " + cases[2].text.strip() + "\n" + "☣ Active cases - " + active + "\n" + "\n" + "*data according to the database that uses worldometers.info/coronavirus/" + "\n" + "*last updated:   " + date, disable_web_page_preview = True)
    elif message.text.lower() == "by country📌":
        flag = 1
        bot.send_message(message.chat.id, "Write the country in which you want to know the number of infected")
    elif flag == 1:
        trans1=(message.text)
        translated1 = translator1.translate(trans1, dest = 'en').text
        if translated1.lower() == "usa":
            translated1 = "us"
        if translated1.lower() == "united kingdom":
            translated1 = "uk"
        if translated1.lower() == "saudi arabia":
            translated1 = "saudi-arabia"
        if translated1.lower() == "south africa":
            translated1 = "south-africa"
        if translated1.lower() == "united arab emirates":
            translated1 = "united-arab-emirates"
        if translated1.lower() == "dominican republic":
            translated1 = "dominican-republic"
        if translated1.lower() == "south korea":
            translated1 = "south-korea"
        res_с = requests.get('https://www.worldometers.info/coronavirus/country/' + translated1.lower()).text
        soup_с = BeautifulSoup(res_с,'html.parser')
        cases_c = soup_с.findAll("div", {"class": "maincounter-number"})
        flag = 0
        translated1 = translated1.capitalize()
        if translated1.lower() == 'us':
            translated1 = 'USA'
        if translated1.lower() == 'south-korea':
            translated1 = 'South Korea'
        if translated1.lower() == "uk":
            translated1 = "United Kingdom"
        if translated1.lower() == "saudi-arabia":
            translated1 = "Saudi Arabia"
        if translated1.lower() == "south-africa":
            translated1 = "South Africa"
        if translated1.lower() == "united-arab-emirates":
            translated1 = "United Arab Emirates"
        if translated1.lower() == "dominican-republic":
            translated1 = "Dominican Republic"
        bot.send_message(message.chat.id, "😷Coronavirus cases in {}:".format(translated1) + "\n" + "\n" + "🦠 Total infected - " + cases_c[0].text.strip() + "\n" + "⚰ Deaths - " + cases_c[1].text.strip() + "\n" + "👥 Recovered - " + cases_c[2].text.strip() + "\n" + "\n" + "*data according to the database that uses worldometers.info/coronavirus/" + "\n" + "*last updated:   " + date, disable_web_page_preview = True)
    
    # #Русский интерфейс
    # elif message.text.lower() == "russian 🇷🇺":
    #     bot.send_message(message.chat.id, "Чтобы узнать о том что может бот и его команды, введите /inforu")
    # elif message.text.lower() == "смена языка🌍":
    #     bot.send_message(message.chat.id, "Приветствую. Чтобы продолжить работу с ботом, выберите язык на клавиатуре ниже", reply_markup=keyboard_lang)
    # elif message.text.lower() == "все числа📊":
    #     bot.send_message(message.chat.id,"🦠 Всего заразившихся - " + cases[0].text.strip() + "\n" + "⚰ Умерших - " + cases[1].text.strip() + "\n" + "👥 Выздоровевших - " + cases[2].text.strip() + "\n" + "☣ Активные случаи - " + active + "\n" + "\n" + "*данные согласно базе данных которую использует worldometers.info/coronavirus/" + "\n" + "*последнее обновление (время указано в gmt/utc +0): \n" + date, disable_web_page_preview = True)
    # elif message.text.lower() == "по стране📌":
    #     flag = 2
    #     bot.send_message(message.chat.id, "Напишите страну в которой вы хотите узнать количество зараженных")
    # elif flag == 2:
    #     trans2=(message.text)
    #     translated2 = translator2.translate(trans2, dest = 'en').text
    #     if translated2.lower() == "usa":
    #         translated2 = "us"
    #     if translated2.lower() == "united kingdom":
    #         translated2 = "uk"
    #     if translated2.lower() == "saudi arabia":
    #         translated2 = "saudi-arabia"
    #     if translated2.lower() == "south africa":
    #         translated2 = "south-africa"
    #     if translated2.lower() == "united arab emirates":
    #         translated2 = "united-arab-emirates"
    #     if translated2.lower() == "dominican republic":
    #         translated2 = "dominican-republic"
    #     if translated2.lower() == "south korea":
    #         translated2 = "south-korea" 
    #     res_с = requests.get('https://www.worldometers.info/coronavirus/country/' + translated2.lower()).text
    #     soup_с = BeautifulSoup(res_с,'html.parser')
    #     cases_c = soup_с.findAll("div", {"class": "maincounter-number"})
    #     flag = 0
    #     translated2 = translated2.capitalize()
    #     if translated2.lower() == 'us':
    #         translated2 = 'USA'
    #     if translated2.lower() == 'south-korea':
    #         translated2 = 'South Korea'
    #     if translated2.lower() == "uk":
    #         translated2 = "United Kingdom"
    #     if translated2.lower() == "saudi-arabia":
    #         translated2 = "Saudi Arabia"
    #     if translated2.lower() == "south-africa":
    #         translated2 = "South Africa"
    #     if translated2.lower() == "united-arab-emirates":
    #         translated2 = "United Arab Emirates"
    #     if translated2.lower() == "dominican-republic":
    #         translated2 = "Dominican Republic"
    #     bot.send_message(message.chat.id, "😷Коронавирусные случаи в {}:".format(translated2) + "\n" + "\n" + "🦠 Всего заразившихся - " + cases_c[0].text.strip() + "\n" + "⚰ Умерших - " + cases_c[1].text.strip() + "\n" + "👥 Выздоровевших - " + cases_c[2].text.strip() + "\n" + "\n" + "*данные согласно базе данных которую использует worldometers.info/coronavirus/" + "\n" + "*последнее обновление (время указано в gmt/utc +0): \n" + date, disable_web_page_preview = True)
    
    #Украинский интерфейс
    elif message.text.lower() == "ukrainian 🇺🇦":
        bot.send_message(message.chat.id, "Щоб дізнатися про те що може бот і його команди, введіть /infoua")
    elif message.text.lower() == "зміна мови🌍":
        bot.send_message(message.chat.id, "Вітаю. Щоб продовжити роботу з ботом, виберіть мову на клавіатурі нижче", reply_markup=keyboard_lang)
    elif message.text.lower() == "всі числа📊":
        bot.send_message(message.chat.id,"🦠 Всього заразилися - " + cases[0].text.strip() + "\n" + "⚰ Померлих - " + cases[1].text.strip() + "\n" + "👥 Видужали - " + cases[2].text.strip() + "\n" + "☣ Активні випадки - " + active + "\n" + "\n" + "*дані згідно з базою даних яку використовує worldometers.info/coronavirus/" + "\n" + "*останнє оновлення (час вказан в gmt/utc +0): \n" + date, disable_web_page_preview = True)
    elif message.text.lower() == "по країні📌":
        flag = 3
        bot.send_message(message.chat.id, "Напишіть країну в якій ви хочете дізнатися кількість заражених")
    elif flag == 3:
        trans3=(message.text)
        translated3 = translator3.translate(trans3, dest = 'en').text
        if translated3.lower() == "usa":
            translated3 = "us"
        if translated3.lower() == "united kingdom":
            translated3 = "uk"
        if translated3.lower() == "saudi arabia":
            translated3 = "saudi-arabia"
        if translated3.lower() == "south africa":
            translated3 = "south-africa"
        if translated3.lower() == "united arab emirates":
            translated3 = "united-arab-emirates"
        if translated3.lower() == "dominican republic":
            translated3 = "dominican-republic"
        if translated3.lower() == "south korea":
            translated3 = "south-korea"
        res_с = requests.get('https://www.worldometers.info/coronavirus/country/' + translated3.lower()).text
        soup_с = BeautifulSoup(res_с,'html.parser')
        cases_c = soup_с.findAll("div", {"class": "maincounter-number"})
        flag = 0
        translated3 = translated3.capitalize()
        if translated3.lower() == 'us':
            translated3 = 'USA'
        if translated3.lower() == 'south-korea':
            translated3 = 'South Korea'
        if translated3.lower() == "uk":
            translated3 = "United Kingdom"
        if translated3.lower() == "saudi-arabia":
            translated3 = "Saudi Arabia"
        if translated3.lower() == "south-africa":
            translated3 = "South Africa"
        if translated3.lower() == "united-arab-emirates":
            translated3 = "United Arab Emirates"
        if translated3.lower() == "dominican-republic":
            translated3 = "Dominican Republic"
        bot.send_message(message.chat.id, "😷Коронавирусні випадки в {}:".format(translated3) + "\n" + "\n" + "🦠 Всього заразилися - " + cases_c[0].text.strip() + "\n" + "⚰ Померлих - " + cases_c[1].text.strip()+ "\n" + "👥 Видужали - " + cases_c[2].text.strip() + "\n" + "\n" + "*дані згідно з базою даних яку використовує worldometers.info/coronavirus/" + "\n" + "*останнє оновлення (час вказан в gmt/utc +0): \n" + date, disable_web_page_preview = True)
bot.polling()
