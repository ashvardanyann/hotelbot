from telebot.types import Message
from loader import bot
from database import DataBase as db


@bot.message_handler(commands=["history"])
def bot_history(message: Message):
    bot.send_message(message.chat.id, db.get_history(message.from_user.id), parse_mode='HTML')
