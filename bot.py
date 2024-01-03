import telebot
import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from info import bot_responses
from data import load_user_data, save_user_data

token = '6453346324:AAFEVDOiWZZn158uhHLVfy5EQb1K228YKQY'
bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)

questions = [
    {"text": "1. Python - это язык программирования?", "options": ["Да", "Нет"]},
    {"text": "2. Переменные в Python можно создавать без явного указания типа данных?", "options": ["Да", "Нет"]},
    {"text": "3. В Python комментарии начинаются с символа '#'", "options": ["Да", "Нет"]},
    {"text": "4. Функция len() используется для определения длины списка в Python?", "options": ["Да", "Нет"]},
    {"text": "5. В Python ключевое слово для определения функции - def?", "options": ["Да", "Нет"]}
]

correct_answers = ["Да", "Да", "Да", "Да", "Да"]

user_answers = []
current_question = 0

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton('Да'))
markup.add(KeyboardButton('Нет'))


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, f"{random.choice(bot_responses['hello'])}.\n"
                                      f"Ты попал на тест по базовому Python. \n"
                                      f"Для полного ознакомления с ботом напишите команду: /help\n"
                                      f"Для начала теста введите команду /test")


@bot.message_handler(commands=['test'])
def create_user(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {}
        user_data[user_id]['username'] = message.from_user.first_name
        user_data[user_id]['test_points'] = 0
        save_user_data(user_data, data_path)
        print(user_id)
        print(user_data)
    elif user_id in user_data:
        bot.send_message(message.chat.id, f"{message.from_user.first_name} рад вас снова видеть, хотите еще пройти тест?")
    start_test(message)


def start_test(message):
    global user_answers, current_question
    user_answers = []
    current_question = 0
    send_question(message.chat.id)


def send_question(chat_id):
    bot.send_message(chat_id, questions[current_question]["text"], reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_answer(message):
    global user_answers, current_question

    if current_question < len(questions):
        user_answers.append(message.text)

        current_question += 1
        if current_question < len(questions):
            send_question(message.chat.id)
        else:
            finish_test(message)
    else:
        bot.send_message(message.chat.id, "Тест уже завершен. Напишите /start, чтобы начать заново.")


def finish_test(message):
    global user_answers, correct_answers
    user_id = str(message.from_user.id)

    score = sum(1 for user, correct in zip(user_answers, correct_answers) if user == correct)
    bot.send_message(message.chat.id, f"Тест завершен!\nВаш результат: {score} из {len(questions)}.")

    user_data[user_id]['test_points'] = score
    print(user_data[user_id]['test_points'])
    save_user_data(user_data, data_path)


bot.polling()
