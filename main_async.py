#!/usr/bin/python

# This is a simple bot using the telebot library
# to interact with the telegram API

import os
import telebot
from telebot.async_telebot import AsyncTeleBot
import utils
import config

bot = AsyncTeleBot(config.API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Что умеет этот бот:
/image - получить изображение с камер
/save - сохранить заметку
/read - прочитать заметку
""")


@bot.message_handler(commands=['image'])
async def iamge_cmd(message):
    for cam in config.LIST_OF_CAMERAS:
        cmd = "ffmpeg -i '" + cam + "' -qscale:v 2 -frames:v 1 -hide_banner -y -loglevel error tmp.jpg"
        os.system(cmd)
        img = open("tmp.jpg", 'rb')
        await bot.send_photo(message.chat.id, img)
        img.close()


@bot.message_handler(commands=['save'])
async def save_cmd(message):
    text = message.text[6:] # Remove '/save '
    if text:
        filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
        if utils.save_to_file(filename, text) == 0:
            await bot.send_message(message.chat.id, "✅ Заметка сохранена")
        else:
            await bot.send_message(message.chat.id, "❌ Ошибка при сохранении заметки")
        return;
    await bot.send_message(message.chat.id, "Введите текст заметки (TODO)")
    # register_next_step_handler() don't work for async bot
    # await bot.register_next_step_handler(message, save_cmd_next_step)

# def save_cmd_next_step(message):
#     filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
#     if utils.save_to_file(filename, message.text) == 0:
#         bot.send_message(message.chat.id, "✅ Заметка сохранена")
#     else:
#         bot.send_message(message.chat.id, "❌ Ошибка при сохранении заметки")


@bot.message_handler(commands=['read'])
async def read_cmd(message):
    filename = os.path.join(os.path.expanduser(config.WORK_DIR), message.from_user.username)
    text = utils.read_from_file(filename)
    if text is None:
        await bot.send_message(message.chat.id, "❌ Ошибка при чтении заметки")
    else:
        await bot.send_message(message.chat.id, "Ваша заметка:")
        await bot.send_message(message.chat.id, text)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)

# Convert path to full path and create dir, if it doesn't exist.
os.makedirs(os.path.expanduser(config.WORK_DIR), exist_ok=True)

import asyncio
asyncio.run(bot.polling())
