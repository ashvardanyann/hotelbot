from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """Создание состояний бота."""
    region = State()
    results_size = State()
    price = State()
    check_in_date = State()
    check_out_date = State()
    adults = State()
    children = State()
