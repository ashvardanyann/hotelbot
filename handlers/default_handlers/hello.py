from telebot.types import Message

from loader import bot

"""Обработчик для сообщения 'привет/Привет',котроый отвечает приветствием"""


@bot.message_handler(func=lambda message: True)
def bot_start(message: Message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    else:
        pass
