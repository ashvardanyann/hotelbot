from api_requests import get_first_hotel_info
from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message

@bot.message_handlers(commands=['low'])
def low(message:Message):
    bot.set_state(message.from_user.id, UserInfoState.region, message.chat.id)
    bot.send_message(message.from_user.id, f'{message.from_user.username}, пожалуйста, введите регион')

@bot.message_handlers(state=UserInfoState.region)
def get_region(message:Message):
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введите количество вариантов отелей')
        bot.set_state(message.from_user.id, UserInfoState.results_size, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['region'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Регион может содержать только буквы')


@bot.message_handlers(state=UserInfoState.results_size)
def get_results_size(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите дату заезда (Например, <b>7-5-2023</b>', parse_mode='HTML')
        bot.set_state(message.from_user.id, UserInfoState.check_in_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['results_size'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество может содержать только числа')

@bot.message_handlers(state=UserInfoState.check_in_date)
def get_check_in_data(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите дату выезда (Например, <b>8-5-2023</b>', parse_mode='HTML')
        bot.set_state(message.from_user.id, UserInfoState.check_out_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['check_in_data'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Дата может содержать только цифры')

@bot.message_handlers(state=UserInfoState.check_out_date)
def get_check_out_data(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите количество взрослых')
        bot.set_state(message.from_user.id, UserInfoState.adults, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['check_out_data'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Дата содержит только цифры')

@bot.message_handlers(state=UserInfoState.adults)
def adults(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите возрасты всех детей. Пример, <b>4,9,6</b>',parse_mode='HTML')
        bot.set_state(message.from_user.id, UserInfoState.children, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество содержит только цифры')
@bot.message_handlers(state=UserInfoState.children)
def children(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал.')


        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['children'] = message.text
            bot.send_message(message.from_user.id, f"{request_info}")
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Содержит только цифры')




#print(get_first_hotel_info('Рига', 3, 'low', '20-7-2023', '21-7-2023', 2, '5,8,7'))

