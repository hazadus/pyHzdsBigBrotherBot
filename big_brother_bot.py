import re
import time

import telebot

import bot_token
import bot_utils
import db_utils
from weather_inform import get_weather_html

bot = telebot.TeleBot(bot_token.TOKEN)

# Список корней матерных слов
f_word_aliases = {
    "Хуй": ["хуй", "хуё", "хуя", "хуе", "хую", "хуи", "хуле", "хули",
            "хyй", "хyё", "хyя", "хyе", "хyю", "хyле", "хyли",  # латиница y
            "xуй", "xуё", "xуя", "xуе", "xую", "xуле", "xули",  # латиница х
            "xyй", "xyё", "xyя", "xyе", "xyю", "xyле", "xyли"  # латиница xy
            ],
    "Пизда": ["пизд", "пизж"],
    "Ебать": ["еба", "еби", "ебл", "ебу", "ёб", "ебы", "ебо", "ебё", "ёпта", "епта", "ёпты", "епты",
              "долбоеб", "долбоёб"],
    "Хер": ["хер"],
    "Блядь": ["бляд", "блят", "блеад", "бляц"],
    "Залупа": ["залуп"],
    "Пидор": ["пидор", "пидар", "педр", "пидр", "педер", "пидер"],
    "Гондон": ["гандон", "гондон"],
    "Манда": ["манда"]
}


def count_f_words(message: telebot.types.Message) -> int:
    """
    Считает и попутно добавляет в БД каждое употребление матерного слова из сообщения.
    Возвращает количество матов в сообщении.
    """

    total_f_count = 0

    # TODO: перед поиском "вычистить" слова типа: требовать, требует, (по)требл(ение), употреблять, мандарин,
    #       мандат...
    for f_key in f_word_aliases.keys():
        for f_value in f_word_aliases[f_key]:
            f_entries = re.findall(f_value, message.text.lower())
            f_value_count = len(f_entries)
            total_f_count = total_f_count + f_value_count

            if total_f_count:
                # на каждое встреченное использование слова добавить строку в БД
                for _ in f_entries:
                    db_utils.db_add_f_message(f_key, message)

    return total_f_count


# TODO: handle image captions (opt+space on "message_handler" below to get info!

@bot.message_handler(content_types=['text'])
def text(message):
    bot_utils.print_debug(message.text, message)

    db_utils.db_add_any_message(message)

    f_count = count_f_words(message)

    if f_count:
        bot_utils.print_debug(f"Найдено матов в сообщении = {f_count}", message)
        bot.reply_to(message, f"{f_count} мата дектед. Алярм!\n\n"
                              f"Ваш счёт: <b>{db_utils.db_get_user_f_word_count(message.from_user.id, message.chat.id)}"
                              f"</b> в этом чате, "
                              f"<b>{db_utils.db_get_user_f_word_count(message.from_user.id)}</b> всего.",
                     parse_mode="HTML")

    # если встречается слово "погод", ответить про погоду в СПБ
    if 'погод' in message.text.lower():
        bot.reply_to(message, 'Да, погода нынче та ещё.\n\n' + get_weather_html())

    # в приватном чате выдаём еще и таблицу рекордов + рейтинг матов на любой текст
    if message.chat.type == 'private':
        f_rating_text = "<b>Рейтинг матерных слов (по всем чатам):</b>\n"
        for row in db_utils.db_get_f_words_rating():
            f_word, score = row
            f_rating_text = f"{f_rating_text}{f_word} - {score}\n"

        bot.reply_to(message, f"<b>Таблица рекордов (по всем чатам):</b>\n"
                              f"{db_utils.db_get_users_score_table()}\n{f_rating_text}",
                     parse_mode="HTML")


while True:
    # noinspection PyBroadException
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
