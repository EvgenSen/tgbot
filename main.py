#!/usr/bin/python

# This is a simple bot using the telebot library
# to interact with the telegram API

import os
import telebot
from telebot import types
import utils
import config

bot = telebot.TeleBot(config.API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Что умеет этот бот:
/image - получить изображение с камер
/save - сохранить заметку
/read - прочитать заметку
/worktime - прочитать инфо о рабочем времени (TODO)\
""")


@bot.message_handler(commands=['image'])
def iamge_cmd(message):
    for cam in config.LIST_OF_CAMERAS:
        cmd = "ffmpeg -i '" + cam + "' -qscale:v 2 -frames:v 1 -hide_banner -y -loglevel error tmp.jpg"
        os.system(cmd)
        img = open("tmp.jpg", 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()


@bot.message_handler(commands=['save'])
def save_cmd(message):
    text = message.text[6:] # Remove '/save '
    if text:
        filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
        if utils.save_to_file(filename, text) == 0:
            bot.send_message(message.chat.id, "✅ Заметка сохранена")
        else:
            bot.send_message(message.chat.id, "❌ Ошибка при сохранении заметки")
        return;
    bot.send_message(message.chat.id, "Введите текст заметки")
    bot.register_next_step_handler(message, save_cmd_next_step)

def save_cmd_next_step(message):
    filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
    if utils.save_to_file(filename, message.text) == 0:
        bot.send_message(message.chat.id, "✅ Заметка сохранена")
    else:
        bot.send_message(message.chat.id, "❌ Ошибка при сохранении заметки")


@bot.message_handler(commands=['read'])
def read_cmd(message):
    filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
    text = utils.read_from_file(filename)
    if text is None:
        bot.send_message(message.chat.id, "❌ Ошибка при чтении заметки")
    else:
        bot.send_message(message.chat.id, "Ваша заметка:")
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['worktime'])
def worktime_cmd(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сегодня")
    btn2 = types.KeyboardButton("Вчера")
    markup.add(btn2, btn1)
    markup.row('Неделя')
    bot.send_message(message.chat.id, "Выберите дату:", reply_markup=markup)
    bot.register_next_step_handler(message, worktime_cmd_next_step)

def worktime_cmd_next_step(message):
    empty_markup = telebot.types.ReplyKeyboardRemove()
    if message.text=="Сегодня":
        bot.send_message(message.chat.id,'Нет информации за этот период (1 TODO)', reply_markup=empty_markup)
    elif message.text=="Вчера":
        bot.send_message(message.chat.id,'Нет информации за этот период (2 TODO)', reply_markup=empty_markup)
    elif message.text=="Неделя":
        bot.send_message(message.chat.id,'Нет информации за этот период (3 TODO)', reply_markup=empty_markup)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

# Convert path to full path and create dir, if it doesn't exist.
os.makedirs(os.path.expanduser(config.WORK_DIR), exist_ok=True)

bot.infinity_polling()
