from api_requests import get_first_hotel_info, get_second_hotel_info
from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message, InputMediaPhoto
from keyboards.inline.hotel_inlinekeyboard import inline_buttons

"""Обработчик кнопок, котрый возвращает фотографии и точный адрес выбранного отеля."""


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    msg = bot.send_message(call.message.chat.id, 'Пожалуйста подождите, идет загрузка ...')
    hotel_details = get_second_hotel_info(call.data)
    media = [InputMediaPhoto(hotel_details['photos'][0], caption=f'Адрес отеля - {hotel_details["address"]}')]
    bot.delete_message(call.message.chat.id, msg.message_id)
    for i in range(1, 5):
        media.append(InputMediaPhoto(hotel_details['photos'][i]))
    bot.send_media_group(call.message.chat.id, media=media)


"""Обработчик команды '/low'"""


@bot.message_handler(commands=['low', 'high'])
def low(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.region, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'{message.from_user.full_name}, пожалуйста, введите регион: (Например, <b>Рига</b>)',
                     parse_mode='HTML')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
        request_info['price_type'] = message.text[1:]
        #print(request_info['price_type'], type(request_info['price_type']))



"""Сохраняем город, введенный пользователем."""


@bot.message_handler(state=UserInfoState.region)
def get_region(message: Message):
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введите количество вариантов отелей')
        bot.set_state(message.from_user.id, UserInfoState.results_size, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['region'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Регион может содержать только буквы')


"""Сохраняем количество вариантов отелей."""


@bot.message_handler(state=UserInfoState.results_size)
def get_results_size(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите дату заезда (Например, <b>7-5-2023</b>)',
                         parse_mode='HTML')
        bot.set_state(message.from_user.id, UserInfoState.check_in_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['results_size'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество может содержать только числа')


"""Сохраняем дату заезда."""


@bot.message_handler(state=UserInfoState.check_in_date)
def get_check_in_data(message: Message):
    bot.send_message(message.from_user.id, 'Спасибо записал. Введите дату выезда (Например, <b>8-5-2023</b>)',
                     parse_mode='HTML')
    bot.set_state(message.from_user.id, UserInfoState.check_out_date, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
        request_info['check_in_data'] = message.text


"""Сохраняем дату выезда"""


@bot.message_handler(state=UserInfoState.check_out_date)
def get_check_out_data(message: Message):
    bot.send_message(message.from_user.id, 'Спасибо записал. Введите количество взрослых')
    bot.set_state(message.from_user.id, UserInfoState.adults, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
        request_info['check_out_data'] = message.text


"""Сохраняем количество взрослых."""


@bot.message_handler(state=UserInfoState.adults)
def adults(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите возрасты всех детей. Пример, <b>4,9,6</b>',
                         parse_mode='HTML')
        bot.set_state(message.from_user.id, UserInfoState.children, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество содержит только цифры')


"""Сохраняем возраст и количество детей и отправляем ввиде кнопок список отелей и их цены."""


@bot.message_handler(state=UserInfoState.children)
def children(message: Message):
    bot.send_message(message.chat.id, 'Спасибо записал.')
    msg = bot.send_message(message.chat.id, 'Пожалуйста подождите, идет загрузка ...')
    #print(msg)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
        hotel_list = get_first_hotel_info(request_info['region'],
                                          request_info['results_size'],
                                          request_info['price_type'],
                                          request_info['check_in_data'],
                                          request_info['check_out_data'],
                                          request_info['adults'],
                                          message.text)
        #print(hotel_list)
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.from_user.id, 'Список отелей:', reply_markup=inline_buttons(hotel_list))
    bot.delete_state(message.from_user.id, message.chat.id)