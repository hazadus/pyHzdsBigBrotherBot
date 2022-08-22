import random
from bs4 import BeautifulSoup as bsoup
import bot_utils


BOT_CHAT_ID = "133637887"  # DebugBot chat with me
# BOT_CHAT_ID = "-1001594961681"  # Пацантрэ


def get_cabbages():
    url = "https://agroserver.ru/kapusta-belokochannaya/p1-city-490.htm"
    # url = "https://agroserver.ru/kapusta-belokochannaya/"
    items = []

    with open('cabbage.html', 'r') as file:
        data = file.read()

    # req = requests.get(url)
    # soup = bsoup(req.text, "html.parser")

    soup = bsoup(data, "html.parser")
    cabbages = soup.find_all("div", class_="tovar")

    for cabbage in cabbages:
        soup1 = bsoup(f"<html>{cabbage}</html>", "html.parser")
        item_desc = ""

        title = soup1.find("div", class_="th")
        if not title == None:
            item_desc = f"<b>{title.text}</b>\n"

        price = soup1.find("div", class_="price")
        if not price == None:
            item_desc = f"{item_desc}<i>{price.text}</i>\n"

        text = soup1.find("div", class_="text")
        if not text == None:
            stripped_text = text.text.replace('\n', ' ')
            item_desc = f"{item_desc}\n{stripped_text}\n"

        seller = soup1.find("div", class_="bl org")
        if not seller == None:
            stripped_text = seller.text.replace('\n', '')
            item_desc = f"{item_desc}\n<i>{stripped_text}</i>\n"

        phones = soup1.find("div", class_="bl phone phone2")
        if not phones == None:
            stripped_text = phones.text.replace('\n', '')
            stripped_text = stripped_text.replace('\t', '')
            item_desc = f"{item_desc}<i>{stripped_text}</i>\n"

        # TODO: parse picture link too
        print(item_desc)
        items.append(item_desc)

    return items


cabbages_list = get_cabbages()
if len(cabbages_list):
    random.shuffle(cabbages_list)
    # TODO: поменять фразу "кстати" на случайно выбранную из нескольких подобных фраз
    bot_utils.bot_sendtext(BOT_CHAT_ID, "Кстати, есть интересные предложения на рынке капусты, например:")
    bot_utils.bot_sendtext(BOT_CHAT_ID, cabbages_list[0])
else:
    print("Some error occured while scraping cabbage prices")
