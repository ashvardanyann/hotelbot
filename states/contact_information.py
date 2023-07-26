from telebot.handler_backends import State, StatesGroup

"""Создание состояний бота."""


class UserInfoState(StatesGroup):
    region = State()
    results_size = State()
    price = State()
    check_in_date = State()
    check_out_date = State()
    adults = State()
    children = State()
