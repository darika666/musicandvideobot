from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)



def button_url(url):
    main_markup = InlineKeyboardMarkup()
    main_markup.add (
        InlineKeyboardButton('audio', callback_data = url))
    main_markup.add (
        InlineKeyboardButton('video', callback_data = url))
    return main_markup


