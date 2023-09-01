from telebot.types import Message
from loader import bot
from database import DataBase as db


@bot.message_handler(commands=["history"])
def bot_history(message: Message):
    """Обработчик для команды /history, который возвращает последние 10 запросов"""
    bot.send_message(message.chat.id, db.get_history(message.from_user.id), parse_mode='HTML')
