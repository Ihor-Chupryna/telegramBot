import telebot
import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from info import bot_responses, locations
from data import load_user_data, save_user_data

token = '6453346324:AAFEVDOiWZZn158uhHLVfy5EQb1K228YKQY'
bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)





@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, f"{random.choice(bot_responses['hello'])}.\n"
                                      f"Ты попал на тест по базовому Python. \n"
                                      f"Для полного ознакомления с ботом напишите команду: /help\n"
                                      f"Для начала теста введите команду /quest")


@bot.message_handler(commands=['quest'])
def create_user(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {}
        user_data[user_id]['username'] = message.from_user.first_name
        save_user_data(user_data, data_path)
        print(user_id)
        print(user_data)
    elif user_id in user_data:
        bot.send_message(message.chat.id, f"{message.from_user.first_name} рад вас снова видеть")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Kingdom Light', callback_data='kingdom_light'))
    keyboard.add(InlineKeyboardButton('Kingdom Dark', callback_data='kingdom_dark'))

    bot.send_message(message.chat.id, "Choose a kingdom:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["kingdom_light", "kingdom_dark"])
def location_selected(call):
    # user_id = str(call.from_user.id)
    if call.data == "kingdom_light":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Forest', callback_data='forest'))
        keyboard.add(InlineKeyboardButton('Desert', callback_data='desert'))

        bot.send_message(call.message.chat.id, f"Welcome to {locations['kingdom_light']['name']}")
        bot.send_photo(call.message.chat.id, open(locations["kingdom_light"]["image"], "rb"))
        bot.send_message(call.message.chat.id, "Kingdom Light. Choose a location:", reply_markup=keyboard)
    elif call.data == "kingdom_dark":
        bot.send_message(call.message.chat.id, "Welcome to Kingdom Dark")
        bot.send_photo(call.message.chat.id, open(locations["kingdom_dark"]["image"], "rb"))
        say_finish(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data in ["forest", "desert"])
def location_selected(call):
    if call.data == "forest":
        bot.send_message(call.message.chat.id, "Forest Hello")
        bot.send_photo(call.message.chat.id, open(locations["forest"]["image"], "rb"))
    elif call.data == "desert":
        bot.send_message(call.message.chat.id, "Desert Hello")
        bot.send_photo(call.message.chat.id, open(locations["desert"]["image"], "rb"))


def say_finish(chat_id):
    bot.send_message(chat_id, "Finish game")


bot.polling()
