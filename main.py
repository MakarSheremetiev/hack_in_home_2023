import logging

import telebot
import datetime
import os
import psycopg2
import requests
from telebot import types
from requests import get
import pandas as pd
from psycopg2 import OperationalError
token = '6621525272:AAH978v_Hwrcs4xLLg7u0JQBt4I0Vs4MGRE'
bot = telebot.TeleBot(token)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error {e} occurred")
    return connection


connection = create_connection('Kaluga_Signal',
                               'makar_shiiishki',
                               'mgH9RdYCoc2j',
                               'ep-lucky-wood-40926738.eu-central-1.aws.neon.tech',
                               '5432')
cursor = connection.cursor()

@bot.message_handler(content_types=['text'], commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Добрый день,'
                                      'Я бот-секретарь,'
                                      'могу помочь Вам найти необходимую документацию.'
                                      'Пожалуйста авторизуйтесь.')
    bot.register_next_step_handler(msg, login_check)


def login_check(message):
    msg = bot.send_message(message.chat.id, 'Пожалуйста введите ваш логин.')
    bot.register_next_step_handler(msg, auth)


def auth(message):
    cursor.execute(f"""SELECT email FROM public.employees where email = '{str(message)}'""")
    res = cursor.fetchone()
    if res:
        msg = bot.send_message(message.chat.id, 'Пожалуйста введите ваш пароль:')
        bot.register_next_step_handler(msg,)
    else:
        msg = bot.send_message(message.chat.id, 'Такого логина нет в базе данных, пожалуйста попробуйте другой')
        bot.register_next_step_handler(msg, login_check())

def password_check(message):
    pass

bot.polling(none_stop=True)