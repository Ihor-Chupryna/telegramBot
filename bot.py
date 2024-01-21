import telebot
import random

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from info import bot_responses, locations
from data import load_user_data, save_user_data

token = '6453346324:AAFEVDOiWZZn158uhHLVfy5EQb1K228YKQY'
bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)


def create_two_button(btn1, btn2):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(telebot.types.KeyboardButton(btn1))
    keyboard.add(telebot.types.KeyboardButton(btn2))
    return keyboard


def create_three_button(btn1, btn2, btn3):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(telebot.types.KeyboardButton(btn1))
    keyboard.add(telebot.types.KeyboardButton(btn2))
    keyboard.add(telebot.types.KeyboardButton(btn3))
    return keyboard


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

        # user_data[user_id]['money'] = 0
        # user_data[user_id]['weapon'] = ""
        # user_data[user_id]['magic'] = ""
        save_user_data(user_data, data_path)
        print(user_id)
        print(user_data)
    elif user_id in user_data:
        bot.send_message(message.chat.id, f"{message.from_user.first_name} рад вас снова видеть,"
                                          f"Modey: {user_data[user_id]['money']} Weapon: {user_data[user_id]['weapon']} ")

    user_data[user_id]['money'] = 0
    user_data[user_id]['weapon'] = ""
    user_data[user_id]['magic'] = ""
    save_user_data(user_data, data_path)

    # keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    # keyboard.add(telebot.types.KeyboardButton('Kingdom Light'))
    # keyboard.add(telebot.types.KeyboardButton('Kingdom Dark'))
    keyboard = create_two_button('Kingdom Light','Kingdom Dark')

    bot.send_message(message.chat.id, f"Choose a kingdom: Kingdom Light or Kingdom Dark", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["Kingdom Light", "Kingdom Dark"])
def location_two(message):
    if message.text == "Kingdom Light":

        user_id = str(message.from_user.id)
        user_data[user_id]['magic'] = False
        save_user_data(user_data, data_path)
        print(user_data)

        # keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        # keyboard.add(telebot.types.KeyboardButton('Forest'))
        # keyboard.add(telebot.types.KeyboardButton('Desert'))
        keyboard = create_two_button('Forest', 'Desert')
        bot.send_message(message.chat.id, f"Welcome to {locations['kingdom_light']['name']}")

        bot.send_photo(message.chat.id, open(locations["kingdom_light"]["image"], "rb"))

        bot.send_message(message.chat.id, f"Kingdom Light. Choose a location: Forest or Desert", reply_markup=keyboard)
    elif message.text == "Kingdom Dark":
        bot.send_message(message.chat.id, "Kingdom Dark")
        bot.send_photo(message.chat.id, open(locations["kingdom_dark"]["image"], "rb"))



@bot.message_handler(func=lambda message: message.text in ["Forest", "Desert"])
def location_three(message):
    if message.text == "Forest":

        # keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        # keyboard.add(telebot.types.KeyboardButton('sword'))
        # keyboard.add(telebot.types.KeyboardButton('spear'))
        # keyboard.add(telebot.types.KeyboardButton('axe'))
        keyboard = create_three_button('sword', 'spear', 'axe')

        bot.send_photo(message.chat.id, open(locations["forest"]["image"], "rb"))
        bot.send_message(message.chat.id, "Forest Hello, take weapon", reply_markup=keyboard)

    elif message.text == 'Desert':
        bot.send_message(message.chat.id, "Desert Hello")
        bot.send_photo(message.chat.id, open(locations["desert"]["image"], "rb"))


@bot.message_handler(func=lambda message: message.text in ["sword", "spear", 'axe'])
def take_weapon(message):
    user_id = str(message.from_user.id)

    if message.text == 'sword':
        bot.send_message(message.chat.id, "You take sword")
        user_data[user_id]['weapon'] = 'sword'
    elif message.text == 'spear':
        bot.send_message(message.chat.id, "You take spear")
        user_data[user_id]['weapon'] = 'spear'
    elif message.text == 'axe':
        bot.send_message(message.chat.id, "You take axe")
        user_data[user_id]['weapon'] = 'axe'

    save_user_data(user_data, data_path)
    print(user_data)
    keyboard = create_two_button("Finish", "Kingdom Dark")
    if user_data[user_id]['magic']:
        bot.send_message(message.chat.id, "Battle with spider, You Win")
    else:
        bot.send_message(message.chat.id, f"Battle with spider, for battle you need magic, if   ...... you must buy in Kingdom Dark", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Finish')
def say_finish(message):
    bot.send_message(message.chat.id, "finish game")

bot.polling()
