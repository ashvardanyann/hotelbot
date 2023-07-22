from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def inline_buttons(hotel_list: list[dict]):
    hotel_keyboards = InlineKeyboardMarkup()
    for data in hotel_list:
        hotel_keyboards.add(InlineKeyboardButton(text=f"{data['name']}-{data['price']}",
                                                 callback_data=data['hotel_id']))

    return hotel_keyboards
