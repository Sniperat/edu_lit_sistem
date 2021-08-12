import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config.settings import BOT_TOKEN

def send_message(text, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    print(response.content)

def sen_query(chat_id):
    keyboard = [
        [
            InlineKeyboardButton("O'zbekcha", callback_data='asd1')
        ],
        [
            InlineKeyboardButton('Русский', callback_data='asd2')
        ],
        [
            InlineKeyboardButton('English', callback_data='asd3')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': 'text', 'reply_markup':{'asd':'asd','er':'as    d'}}
    response = requests.post(url, data=data)