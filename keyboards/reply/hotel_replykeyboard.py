from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def children_button() -> ReplyKeyboardMarkup:
    """Функция создания 'reply' клавиатуры."""
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Нет детей'))
    return keyboard
