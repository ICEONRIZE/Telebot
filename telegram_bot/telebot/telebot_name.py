import telebot
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

icebot = telebot.TeleBot('7462905168:AAH5pNNOA9sfEejp8EFJypZsdTfdKusJ9uo')
# dp = Dispatcher(icebot)

users = {}


# Start of bot program
@icebot.message_handler(func=lambda message: message.text == 'Hello' or message.text == 'hello')
def start(message):
    chat_id = message.chat.id
    ice_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    schedule_button = telebot.types.KeyboardButton(text='Make a schedule')
    chat_button = telebot.types.KeyboardButton(text='Bot chat')
    mini_game_button = telebot.types.KeyboardButton(text='Mini game')
    file_share_button = telebot.types.KeyboardButton(text='File sharing')
    web_sites_button = telebot.types.KeyboardButton(text='Web-sites')
    help_button = telebot.types.KeyboardButton(text='Help')
    ice_keyboard.add(chat_button, schedule_button,
                     mini_game_button, file_share_button, help_button)
    icebot.send_message(chat_id,
                        'Welcome! My name is ICEBOT! Here is function that u can use',
                        reply_markup=ice_keyboard)


# Bot chatting function
@icebot.message_handler(func=lambda message: message.text == 'Bot chat')
def chat_bot_function(message):
    chat_id = message.chat.id
    icebot.send_message(chat_id,
                        'Hello! My name is ICEBOT, what is your name?')
    users[chat_id] = {}
    icebot.register_next_step_handler(message, save_username)


# Bot chatting: Name entering
def save_username(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id]['name'] = name
    icebot.send_message(chat_id,
                        f'Perfect, {name}. Can you let me know your surname')
    icebot.register_next_step_handler(message, save_surname)


# Bot chatting: Surname entering
def save_surname(message):
    chat_id = message.chat.id
    surname = message.text
    users[chat_id]['surname'] = surname
    icebot.send_message(chat_id, f'Your data was successfully saved!')


# Delegate: Bot chatting: Data checking
@icebot.message_handler(func=lambda message: message.text == 'Who am i?' or message.text == 'who am i?')
def who_i(message):
    chat_id = message.chat.id
    name = users[chat_id]['name']
    surname = users[chat_id]['surname']
    ice_inline_keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton(text='Yes/Save', callback_data='save_data')
    button_no = telebot.types.InlineKeyboardButton(text='No/Change', callback_data='change_data')
    ice_inline_keyboard.add(button_yes, button_no)
    icebot.send_message(chat_id, f'You are: {name} {surname}', reply_markup=ice_inline_keyboard)


# Delegate: Bot chatting: Saving data
@icebot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    icebot.send_message(chat_id, f'Your data saved')


# Delegate: Bot chatting: Changing data
@icebot.callback_query_handler(func=lambda call: call.data == 'change_data')
def change_btn(call):
    message = call.message
    chat_id = message.chat.id
    icebot.send_message(chat_id, f'Change data')
    chat_bot_function(message)


# Delegate: Keyboard removing
@icebot.message_handler(commands=['remove_keyboard'])
def remove_keyboard(message):
    chat_id = message.chat.id
    ice_keyboard = telebot.types.ReplyKeyboardRemove()
    icebot.send_message(chat_id,
                        'I deleted keyboard!',
                        reply_markup=ice_keyboard)


# Delegate: Helping function
@icebot.message_handler(func=lambda message: message.text == 'Help')
def help_function(message):
    chat_id = message.chat.id
    ice_help_inline_keyboard = telebot.types.InlineKeyboardMarkup()
    remove_keyboard_button = telebot.types.InlineKeyboardButton(text='/remove_keyboard',
                                                                callback_data='remove_keyboard')
    checking_button = telebot.types.InlineKeyboardButton(text='who am i?', callback_data='who_am_i_?')
    ice_help_inline_keyboard.add(remove_keyboard_button, checking_button)
    icebot.send_message(chat_id, f'You can choose following functions. '
                        f'Click to button down bellow to read function description',
                        reply_markup=ice_help_inline_keyboard)


@icebot.callback_query_handler(func=lambda call: call.data == 'remove_keyboard')
def remove_keyboard_callback(call):
    message = call.message
    chat_id = message.chat.id
    icebot.send_message(chat_id, f'You can remove the keyboard using this function')


@icebot.callback_query_handler(func=lambda call: call.data == 'who_am_i_?')
def check_data_callback(call):
    message = call.message
    chat_id = message.chat.id
    icebot.send_message(chat_id, f'You can use this function to check entered data')


if __name__ == '__main__':
    print('Bot is working!')
    icebot.infinity_polling()