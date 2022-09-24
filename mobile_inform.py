import requests
import random

from bs4 import BeautifulSoup

from bot_utils import bot_sendtext


# BOT_CHAT_ID = "133637887"  # DebugBot chat with me
BOT_CHAT_ID = "-1001594961681"  # Пацантрэ
# BOT_CHAT_ID = "-1001726929655"  # MTG

intros = [
    'Вести с полей:',
    'Сушите портянки?',
    'Вещички собрали уже?',
    'Кому-то из знакомых уже вручили повестки?',
    'Товарищ майор не дремлет:',
    'Что там в РЖД с призывом?'
]


def google_search(query: str, max_results: int) -> dict:
    url = f"https://www.google.com/search?q={query}&num={max_results}"
    req = requests.get(url)
    html = BeautifulSoup(req.content, "html.parser")
    links = html.find_all("a")
    results = dict()

    for result in links:
        href = result.get('href')
        if "url?q=" in href and not "webcache" in href:
            title = result.find_all('h3')
            if len(title) != 0:
                url = result.get('href')
                url = url.split("&")[0]
                url = url.split("url?q=")[1]
                results.update({title[0].text: url})
    return results


if __name__ == '__main__':
    found = google_search('мобилизация в санкт-петербурге', 10)
    if len(found) != 0:
        msg_html = '\n'.join([f'\U0001FA96 [ <a href="{link}">{title}</a> ]' for title, link in found.items()])
        bot_sendtext(BOT_CHAT_ID, random.choice(intros))
        print(found)
        print(msg_html)
        bot_sendtext(BOT_CHAT_ID, msg_html)
    else:
        bot_sendtext(BOT_CHAT_ID, 'Какие новости по мобилизации?')
