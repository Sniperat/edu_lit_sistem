import requests
from config.settings import BOT_TOKEN

def send_message(text, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    print(response.content)
