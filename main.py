#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import os
import telebot
import utils
import config

bot = telebot.TeleBot(config.API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
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
            bot.send_message(message.chat.id, "Заметка сохранена")
        else:
            bot.send_message(message.chat.id, "Ошибка при сохранении заметки")
        return;
    bot.send_message(message.chat.id, "Введите текст заметки")
    bot.register_next_step_handler(message, save_cmd_next_step)

def save_cmd_next_step(message):
    filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
    if utils.save_to_file(filename, message.text) == 0:
        bot.send_message(message.chat.id, "Заметка сохранена")
    else:
        bot.send_message(message.chat.id, "Ошибка при сохранении заметки")


@bot.message_handler(commands=['read'])
def read_cmd(message):
    filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
    text = utils.read_from_file(filename)
    if text is None:
        bot.send_message(message.chat.id, "Ошибка при чтении заметки")
    else:
        bot.send_message(message.chat.id, "Ваша заметка:")
        bot.send_message(message.chat.id, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

# Convert path to full path and create dir, if it doesn't exist.
os.makedirs(os.path.expanduser(config.WORK_DIR), exist_ok=True)

bot.infinity_polling()
