import re
import time
import telebot
from datetime import datetime
import bot_token


IS_DEBUG = True

# Список корней матерных слов
f_word_aliases = {
    "Хуй": ["хуй", "хуё", "хуя", "хуе", "хую"],
    "Пизда": ["пизд", "пизж"],
    "Ебать": ["еба", "еби", "ебл", "ебу", "ёб", "ебы", "ебо"],
    "Хер": ["хер"],
    "Блядь": ["бляд", "блят", "блеад", "бляц"],
    "Залупа": ["залуп"],
    "Пидор": ["пидор", "пидар", "педр", "пидр"],
    "Гондон": ["гандон", "гондон"],
    "Манда": ["манда"]  # TODO: подумать как отделить мандарин, мандат?
}

bot = telebot.TeleBot(bot_token.TOKEN)


def print_debug(message):
    if IS_DEBUG:
        print(message)


print_debug(f_word_aliases.keys())


def count_f_words(offensive_text):
    total_f_count = 0

    for f_key in f_word_aliases.keys():
        # print_debug(f"{f_key} has {len(f_word_aliases[f_key])} values")
        for f_value in f_word_aliases[f_key]:
            f_value_count = len(re.findall(f_value, offensive_text.lower()))
            # print_debug(f" - {f_value} : {f_value_count} entries")
            total_f_count = total_f_count + f_value_count

    return total_f_count


@bot.message_handler(content_types=['text'])
def text(message):
    print_debug(datetime.now().strftime('>>> %d %b %Y %H:%M (') + str(message.chat.type) + " "
                + str(message.chat.id) + "): " + message.text)

    f_count = count_f_words(message.text)

    if f_count:
        print_debug(f"f_count = {f_count}")
        bot.reply_to(message, f"{f_count} мата дектед. Алярм!", parse_mode="HTML")


while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
