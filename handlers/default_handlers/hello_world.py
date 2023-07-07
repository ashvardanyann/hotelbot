from telebot.types import Message

from loader import bot

"""Обработчик команды /hello_world, котрый реагирует на команду приветствием"""


@bot.message_handler(commands=["hello_world"])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
