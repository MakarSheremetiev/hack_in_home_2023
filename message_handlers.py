# message_handlers.py
from telebot import types
import telebot
from main import bot, cursor, connection
from database import connect_to_database

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Авторизация')
    markup.add(itembtn1)
    bot.send_message(message.chat.id,
                     'Добрый день,\n'
                     'Я бот-секретарь,\n'
                     'могу помочь Вам найти необходимую документацию.\n'
                     'Пожалуйста авторизуйтесь.', reply_markup=markup)



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Авторизация')
    markup.add(itembtn1)
    bot.send_message(message.chat.id,
                     'Добрый день,\n'
                     'Я бот-секретарь,\n'
                     'могу помочь Вам найти необходимую документацию.\n'
                     'Пожалуйста авторизуйтесь.', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Авторизация')
def ask_phone(message):
    bot.send_message(message.chat.id, 'Введите свой номер телефона по шаблону (+79*********)')
    bot.register_next_step_handler(message, check_phone)

def check_phone(message):
    phone = message.text
    if not phone.startswith('+79') or len(phone) != 13:
        bot.send_message(message.chat.id, 'Неверный формат номера. Попробуйте еще раз.')
        bot.register_next_step_handler(message, check_phone)
        return

    cursor.execute(f"SELECT * FROM employees WHERE phone = '{phone}'")
    user = cursor.fetchone()
    if user:
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, check_password, user)
    else:
        bot.send_message(message.chat.id, 'Такого номера нет в базе данных. Попробуйте еще раз.')
        bot.register_next_step_handler(message, check_phone)

def check_password(message, user):
    password = message.text
    if user[1] == 2:
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Найти документ')
        markup.add(itembtn1)
        if password == user[5]:  # предполагая, что пароль находится в 6-й колонке
            bot.send_message(message.chat.id, 'Вы успешно авторизовались!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неверный пароль, введите пароль заново')
            bot.register_next_step_handler(message, check_password, user)
    elif user[1] == 1:
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Найти документ')
        itembtn2 = types.KeyboardButton('Предоставить права')
        itembtn3 = types.KeyboardButton('Добавить документ')
        markup.add(itembtn1, itembtn2, itembtn3)
        if password == user[5]:  # предполагая, что пароль находится в 6-й колонке
            bot.send_message(message.chat.id, 'Вы успешно авторизовались!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неверный пароль, введите пароль заново')
            bot.register_next_step_handler(message, check_password, user)
# После успешной авторизации

@bot.message_handler(func=lambda message: message.text == 'Найти документ')
def find_document(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('тип')
    itembtn2 = types.KeyboardButton('номер')
    itembtn3 = types.KeyboardButton('название')
    itembtn4 = types.KeyboardButton('дата выхода')
    itembtn5 = types.KeyboardButton('дата ввода действие')
    itembtn6 = types.KeyboardButton('ключевые слова')
    itembtn7 = types.KeyboardButton('назад')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
    bot.send_message(message.chat.id, "Выберите по какому полю хотите искать документ:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Предоставить права')
def predostav_prava(message):
    bot.send_message(message.chat.id, "Введите номер сотрудника, кому хотите предоставить права администратора:")
    bot.register_next_step_handler(message, update_role)

def update_role(message):
    phone_num = message.text
    if not phone_num.startswith('+79') or len(phone_num) != 13:
        bot.send_message(message.chat.id, 'Неверный формат номера. Попробуйте еще раз.')
        bot.register_next_step_handler(message, update_role)
        return

    cursor.execute(f"SELECT * FROM employees WHERE phone = '{phone_num}'")
    user = cursor.fetchone()
    if user:
        cursor.execute(f"""UPDATE employees SET role_id = 1  WHERE phone = '{str(phone_num)}'""")
        connection.commit()
        bot.send_message(message.chat.id, 'Отлично, права предоставлены!')
        bot.register_next_step_handler(message, check_password, phone_num)
    else:
        bot.send_message(message.chat.id, 'Такого номера нет в базе данных. Попробуйте еще раз.')
        bot.register_next_step_handler(message, update_role)


@bot.message_handler(func=lambda message: message.text in ['тип', 'номер', 'название','дата выхода','дата ввода действие', 'ключевые слова'])
def enter_search_criteria(message):
    if message.text == 'тип':
        bot.send_message(message.chat.id, "Введите тип, который хотите найти:")
        bot.register_next_step_handler(message, search_by_type)
    elif message.text == 'номер':
        bot.send_message(message.chat.id, "Введите номер, который хотите найти:")
        bot.register_next_step_handler(message, search_by_number)
    elif message.text == 'название':
        bot.send_message(message.chat.id, "Введите название, который хотите найти:")
        bot.register_next_step_handler(message, search_by_title)
    elif message.text == 'дата выхода':
        bot.send_message(message.chat.id, "Введите дату выхода, который хотите найти:")
        bot.register_next_step_handler(message, search_by_date_out)
    elif message.text == 'дата ввода действие':
        bot.send_message(message.chat.id, "Введите дату ввода действие, который хотите найти:")
        bot.register_next_step_handler(message, search_by_date_inp)
    elif message.text == 'ключевые слова':
        bot.send_message(message.chat.id, "Введите ключевые слова, который хотите найти:")
        bot.register_next_step_handler(message, search_by_key_word)
    elif message.text == 'назад':
        bot.send_message(message.chat.id, "Вы вернулись в основное меню:")
        bot.register_next_step_handler(message, find_document)





def search_by_type(message):
    # Запрос к БД
    cursor.execute(f"""SELECT d.documentlink FROM documents d JOIN documenttypes dt ON d.typeid = dt.id WHERE dt.typename LIKE '%{message.text}%'""")
    results = cursor.fetchall()
    send_results_to_user(message, results)


def search_by_number(message):
    # Запрос к БД
    cursor.execute(f"""SELECT documentlink FROM documents WHERE number LIKE '%{message.text}%'""")
    results = cursor.fetchall()
    send_results_to_user(message, results)

def search_by_title(message):
    # Запрос к БД
    cursor.execute(f"""SELECT documentlink FROM documents WHERE title LIKE '%{message.text}%'""")
    results = cursor.fetchall()
    send_results_to_user(message, results)

def search_by_date_out(message):
    # Запрос к БД
    cursor.execute(f"""SELECT documentlink FROM documents WHERE releasedate = TO_DATE('{message.text}', 'YYYY-MM-DD')""")
    results = cursor.fetchall()
    send_results_to_user(message, results)

def search_by_date_inp(message):
    # Запрос к БД
    cursor.execute(f"""SELECT documentlink FROM documents WHERE startdate = TO_DATE('{message.text}', 'YYYY-MM-DD')""")
    results = cursor.fetchall()
    send_results_to_user(message, results)

def search_by_key_word(message):
    # Запрос к БД
    cursor.execute(f"""select d.documentlink  from keywords k join documents d on k.id = d.id where k.keyword  number LIKE '%{message.text}%'""")
    results = cursor.fetchall()
    send_results_to_user(message, results)


def send_results_to_user(message, results):
    if len(results) == 1:
        bot.send_document(message.chat.id, open(results[0][0], 'rb'))
    elif 1 < len(results) <= 5:
        for result in results:
            bot.send_document(message.chat.id, open(result[0], 'rb'))
    elif len(results) > 5:
        bot.send_message(message.chat.id, f"Найдено {len(results)} документов. Уточните ваш запрос.")
        find_document()



@bot.message_handler(content_types=['text'])
def unknown_message(message):
    bot.send_message(message.chat.id, "Такую функцию бот не знает")
