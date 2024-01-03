import telebot
import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from info import bot_responses
from data import load_user_data, save_user_data

token = '6453346324:AAFEVDOiWZZn158uhHLVfy5EQb1K228YKQY'
bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)

test_counter = 0

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton('Да'))
markup.add(KeyboardButton('Нет'))


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, f"{random.choice(bot_responses['hello'])}.\n"
                                      f"Ты попал на тест по базовому Python. \n"
                                      f"Для полного ознакомления с ботом напишите команду: /help\n"
                                      f"Для начала теста введите команду /test")

    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {}
        user_data[user_id]['username'] = message.from_user.first_name
        user_data[user_id]['test_points'] = 0
        save_user_data(user_data, data_path)
        print(user_id)
        print(user_data)
    elif user_id in user_data:
        bot.send_message(message.chat.id, f"{message.from_user.first_name} рад вас снова видеть")


@bot.message_handler(commands=['test'])
def first_question(message):
    bot.send_message(message.chat.id, 'Число может быть ключем в словаре Python?', reply_markup=markup)


@bot.message_handler()
def first_answer_second_question(message):
    if message.text == 'Да':
        global test_counter
        test_counter += 1
        print(test_counter)
    bot.send_message(message.chat.id, 'Ключевое слово Return останавливает выполнение функции?', reply_markup=markup)


@bot.message_handler()
def second_answer_third_question(message):
    if message.text == 'Да':
        global test_counter
        test_counter += 1
        print(test_counter)
    bot.send_message(message.chat.id, 'Список(list) имеет упорядоченый набор элементов', reply_markup=markup)


bot.polling()
