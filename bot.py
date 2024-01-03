import telebot
import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from info import bot_responses
from data import load_user_data, save_user_data

token = '6453346324:AAFEVDOiWZZn158uhHLVfy5EQb1K228YKQY'
bot = telebot.TeleBot(token=token)

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
markup.add(KeyboardButton('Да'), KeyboardButton('Нет'))

# keyboard = InlineKeyboardMarkup()
# keyboard.add(InlineKeyboardButton('Да', callback_data='Да'), InlineKeyboardButton('Нет', callback_data='Нет'))


@bot.message_handler(commands=['start'])
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
            finish_test(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Тест уже завершен. Напишите /start, чтобы начать заново.")


def finish_test(chat_id):
    global user_answers, correct_answers

    score = sum(1 for user, correct in zip(user_answers, correct_answers) if user == correct)
    bot.send_message(chat_id, f"Тест завершен!\nВаш результат: {score} из {len(questions)}.")


bot.polling()
