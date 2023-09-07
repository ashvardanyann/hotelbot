from loader import bot
import handlers # noqa
from database.main import DataBase as db
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands


if __name__ == "__main__":
    db.create_db()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
