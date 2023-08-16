from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def children_button() -> ReplyKeyboardMarkup:
    """Функция создания 'reply' клавиатуры с названием 'Нет детей'."""
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Нет детей'))
    return keyboard
