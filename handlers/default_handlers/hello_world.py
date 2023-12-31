from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["hello_world"])
def bot_start(message: Message):
    """Обработчик команды /hello_world, который реагирует на команду приветствием"""
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
