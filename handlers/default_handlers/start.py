from telebot.types import Message
from database import DataBase
import datetime
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Обработчик команды '/start', который отвечает приветствием."""
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    db = DataBase()
    db.add_user(message.from_user.id, message.from_user.full_name)
    # with db.db:
    #     db.User(tg_user_id=message.from_user.id,
    #             user_name=message.from_user.full_name,
    #             start_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).save()
        #print(db.User.get(db.User.id.desc()).start_datetime)

