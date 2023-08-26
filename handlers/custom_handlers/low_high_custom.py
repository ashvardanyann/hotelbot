from api_requests import get_first_hotel_info, get_second_hotel_info
from loader import bot
from states.user_states import UserStates
from telebot.types import Message, InputMediaPhoto, ReplyKeyboardRemove
from keyboards.inline.hotel_inlinekeyboard import inline_buttons
from keyboards.reply.hotel_replykeyboard import children_button
import re
from database import DataBase as db

# Создаем паттерны для регулярных выражений
pattern1 = r'^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([0-9]{4})$'
pattern2 = r'^(\d{1,2})(,\d{1,2})*$'
pattern3 = r"^\d+-\d+$"


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработчик кнопок, который возвращает фотографии и точный адрес выбранного отеля."""
    msg = bot.send_message(call.message.chat.id, 'Пожалуйста подождите, идет загрузка ...')
    hotel_details = get_second_hotel_info(call.data)
    media = [InputMediaPhoto(hotel_details['photos'][0], caption=f'Адрес отеля - {hotel_details["address"]}')]
    bot.delete_message(call.message.chat.id, msg.message_id)
    for data in range(1, 5):
        media.append(InputMediaPhoto(hotel_details['photos'][data]))
    bot.send_media_group(call.message.chat.id, media=media)


@bot.message_handler(commands=['low', 'high', 'custom'])
def low_high_custom(message: Message):
    """Обработчик команд /low, /high и /custom который сохраняет тип команды и ставит бота в состояние region."""
    bot.set_state(message.from_user.id, UserStates.region, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'{message.from_user.full_name}, пожалуйста, введите регион: (Например, <b>Рига</b>).',
                     parse_mode='HTML')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
        request_info['price_type'] = message.text[1:]


@bot.message_handler(state=UserStates.region)
def get_region(message: Message):
    """Сохраняем город, введенный пользователем и ставим бота в состояние results_size."""
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введите количество вариантов отелей.')
        bot.set_state(message.from_user.id, UserStates.results_size, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['region'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Регион может содержать только буквы.')


@bot.message_handler(state=UserStates.results_size)
def get_results_size(message: Message):
    """Сохраняем количество вариантов отелей, и ставим бота в состояние check_in_date."""
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите дату заезда (Например, <b>07-05-2023</b>).',
                         parse_mode='HTML')
        bot.set_state(message.from_user.id, UserStates.check_in_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['results_size'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество может содержать только числа.')


@bot.message_handler(state=UserStates.check_in_date)
def get_check_in_data(message: Message):
    """Сохраняем дату заезда, и ставим бота в состояние check_out_date."""
    if re.match(pattern1, message.text):
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите дату выезда (Например, <b>08-05-2023</b>).',
                         parse_mode='HTML')
        bot.set_state(message.from_user.id, UserStates.check_out_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['check_in_data'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, пишите в правильном формате.')


@bot.message_handler(state=UserStates.check_out_date)
def get_check_out_data(message: Message):
    """Сохраняем дату выезда, и ставим бота в состояние adults."""
    if re.match(pattern1, message.text):
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите количество взрослых.')
        bot.set_state(message.from_user.id, UserStates.adults, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['check_out_data'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, пишите в правильном формате.')


@bot.message_handler(state=UserStates.adults)
def adults(message: Message):
    """Сохраняем количество взрослых, и ставим бота в состояние children."""
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Введите возрасты всех детей (Например, <b>4,9,6</b>).',
                         parse_mode='HTML',
                         reply_markup=children_button())
        bot.set_state(message.from_user.id, UserStates.children, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            request_info['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество содержит только цифры.')


@bot.message_handler(state=UserStates.children)
def children(message: Message):
    """Сохраняем возраст и количество детей и отправляем ввиде кнопок список отелей и их цены если тип команды /low либо
    /high, а при команде /custom, ставим бота в состояние price."""
    if re.match(pattern2, message.text) or message.text == 'Нет детей':

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            if request_info['price_type'] == 'custom':
                bot.send_message(message.from_user.id,
                                 'Спасибо записал. Введите желаемый ценовой диапазон в долларах (Например, <b>100-150</b>).',
                                 parse_mode='HTML')
                request_info['children'] = message.text
                bot.set_state(message.from_user.id, UserStates.price, message.chat.id)
                return None
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста подождите, идет загрузка ...',
                                       reply_markup=ReplyKeyboardRemove(selective=False))
                request_info['children'] = message.text
                hotel_list = get_first_hotel_info(request_info['region'],
                                                  request_info['results_size'],
                                                  request_info['price_type'],
                                                  request_info['check_in_data'],
                                                  request_info['check_out_data'],
                                                  request_info['adults'],
                                                  request_info['children'])
                bot.delete_message(message.chat.id, msg.message_id)
                bot.send_message(message.from_user.id, 'Список отелей:', reply_markup=inline_buttons(hotel_list))
                db.save_action(message.from_user.id, request_info)
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, пишите в правильном формате.')


@bot.message_handler(state=UserStates.price)
def price(message: Message):
    """Сохраняем ценовой диапазон и отправляем ввиде кнопок список отелей и их цены."""
    if re.match(pattern3, message.text):

        with bot.retrieve_data(message.from_user.id, message.chat.id) as request_info:
            msg = bot.send_message(message.chat.id, 'Пожалуйста подождите, идет загрузка ...',
                                   reply_markup=ReplyKeyboardRemove(selective=False))
            request_info['price_diopozon'] = message.text
            hotel_list = get_first_hotel_info(request_info['region'],
                                              request_info['results_size'],
                                              request_info['price_type'],
                                              request_info['check_in_data'],
                                              request_info['check_out_data'],
                                              request_info['adults'],
                                              request_info['children'],
                                              request_info['price_diopozon'])
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.from_user.id, 'Список отелей:', reply_markup=inline_buttons(hotel_list))
            db.save_action(message.from_user.id, request_info, price=request_info['price_diopozon'])
        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, пишите в правильном формате.')
