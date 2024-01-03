import telebot
import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from info import bot_responses
from data import load_user_data, save_user_data

token = '6453346324:AAFEVDOiWZZn158uhHLVfy5EQb1K228YKQY'
bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)

test_counter = 0

# markup = ReplyKeyboardMarkup(resize_keyboard=True)
# markup.add(KeyboardButton('Да'))
# markup.add(KeyboardButton('Нет'))

questions = [
    "Вопрос 1: Python — это язык программирования?",
    "Вопрос 2: Python поддерживает множественное наследование?",
    "Вопрос 3: В Python можно использовать скобки для создания блоков кода?",
    "Вопрос 4: Python имеет встроенные средства для работы с регулярными выражениями?",
    "Вопрос 5: Python - это интерпретируемый язык программирования?"
]

correct_answers = ['Да', 'Да', 'Нет', 'Да', 'Да']

# Создаем словарь для хранения ответов пользователя
user_responses = {}


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


# @bot.message_handler(commands=['test'])
# def first_question(message):
#     user_id = str(message.from_user.id)
#     if user_id not in user_data:
#         user_data[user_id] = {}
#         user_data[user_id]['username'] = message.from_user.first_name
#         user_data[user_id]['test_points'] = 0
#         save_user_data(user_data, data_path)
#         print(user_id)
#         print(user_data)
#     elif user_id in user_data:
#         bot.send_message(message.chat.id, f"{message.from_user.first_name} рад вас снова видеть")


# Функция для начала теста
@bot.message_handler(commands=['test'])
def start_test(message):
    user_id = str(message.from_user.id)
    user_responses[user_id] = {'score': 0, 'current_question': 0}
    ask_question(message)


# Функция для задания вопроса


def ask_question(message):
    user_id = str(message.from_user.id)
    current_question = user_responses[user_id]['current_question']

    if current_question < len(questions):
        question_text = questions[current_question]
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Да', callback_data='yes'),
                     InlineKeyboardButton('Нет', callback_data='no'))

        bot.send_message(message.chat.id, question_text, reply_markup=keyboard)
    else:
        finish_test(message)


# Функция для обработки ответа пользователя


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = str(call.from_user.id)
    current_question = user_responses[user_id]['current_question']
    user_responses[user_id]['current_question'] += 1

    # Проверяем, правильный ли ответ
    if call.data == correct_answers[current_question]:
        user_responses[user_id]['score'] += 1

    ask_question(call.message)


# Функция для завершения теста


def finish_test(message):
    user_id = str(message.from_user.id)
    score = user_responses[user_id]['score']
    bot.send_message(message.chat.id, f"Тест завершен!\nВаш результат: {score} из {len(questions)}")


bot.polling()
