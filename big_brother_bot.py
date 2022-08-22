import re
import time
import telebot
import bot_token
import bot_utils
import db_utils


# TODO: формировать рейтинг юзеров по матершине (функция в pyTelegramBot набросана + cron?)
#       рейтинг глобальный и отдельно для конкретного чата?
# TODO: запланированное сообщение (утром и вечером) с выводом рейтинга юзеров (наброски в pyMysqlDemo)
# TODO: фиксировать вообще _все_ сообщения в отдельной таблице (для дальнейшего анализа)


bot = telebot.TeleBot(bot_token.TOKEN)

# Список корней матерных слов
f_word_aliases = {
    "Хуй": ["хуй", "хуё", "хуя", "хуе", "хую", "хуле", "хули"],
    "Пизда": ["пизд", "пизж"],
    "Ебать": ["еба", "еби", "ебл", "ебу", "ёб", "ебы", "ебо", "ёпта", "епта", "ёпты", "епты"],
    "Хер": ["хер"],
    "Блядь": ["бляд", "блят", "блеад", "бляц"],
    "Залупа": ["залуп"],
    "Пидор": ["пидор", "пидар", "педр", "пидр", "педер", "пидер"],
    "Гондон": ["гандон", "гондон"],
    "Манда": ["манда"]  # TODO: подумать как отделить мандарин, мандат?
}


def count_f_words(message: telebot.types.Message) -> int:
    """
    Считает и попутно добавляет в БД каждое употребление матерного слова из сообщения.
    Возвращает количество матов в сообщении.
    """

    total_f_count = 0

    for f_key in f_word_aliases.keys():
        for f_value in f_word_aliases[f_key]:
            f_entries = re.findall(f_value, message.text.lower())
            f_value_count = len(f_entries)
            total_f_count = total_f_count + f_value_count

            if total_f_count:
                # на каждое встреченное использование слова добавить строку в БД
                for f_entry in f_entries:
                    db_utils.db_add_f_message(f_key, message)

    return total_f_count


@bot.message_handler(content_types=['text'])
def text(message):
    bot_utils.print_debug(message.text, message)

    f_count = count_f_words(message)

    if f_count:
        bot_utils.print_debug(f"Найдено матов в сообщении = {f_count}", message)
        bot.reply_to(message, f"{f_count} мата дектед. Алярм!\n\n"
                              f"Ваш счёт: <b>{db_utils.db_get_user_f_word_count(message.from_user.id)}</b>", parse_mode="HTML")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
