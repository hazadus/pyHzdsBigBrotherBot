import bot_token
import requests
from datetime import datetime


def print_debug(text: str, message=None) -> None:
    if message is None:
        print(datetime.now().strftime('%d %b %Y %H:%M:%S ') + text)
    else:
        print(datetime.now().strftime('%d %b %Y %H:%M:%S (') + str(message.chat.type)
              + " " + str(message.chat.id)
              + f" {message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}"
              + "): " + text)


def bot_sendtext(chat_id: str, bot_message: str) -> None:
    """Отправляет текст от имени бота в чат через Telegram HTTP API"""

    send_text = 'https://api.telegram.org/bot' + bot_token.TOKEN \
                + '/sendMessage?chat_id=' + chat_id \
                + '&parse_mode=HTML&text=' \
                + bot_message
    request = requests.get(send_text)
    print_debug(request.text)
