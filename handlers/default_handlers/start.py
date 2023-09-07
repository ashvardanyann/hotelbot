from telebot.types import Message
from database.main import DataBase
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Обработчик команды '/start', который отвечает приветствием."""
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    db = DataBase()
    db.add_user(message.from_user.id, message.from_user.full_name)

