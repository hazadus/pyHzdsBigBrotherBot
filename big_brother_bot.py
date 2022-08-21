import re
import time
import telebot
from datetime import datetime
import bot_token
from mysql.connector import connect, Error


# TODO: добавить к функциям грамотные комменты https://realpython.com/documenting-python-code/
# TODO: формировать рейтинг юзеров по матершине (функция в pyTelegramBot набросана + cron?)
# ----- рейтинг глобальный и отдельно для конкретного чата?
# TODO: запланированное сообщение (утром и вечером) с выводом рейтинга юзеров (наброски в pyMysqlDemo)
# TODO: фиксировать вообще _все_ сообщения в отдельной таблице (для дальнейшего анализа)

IS_DEBUG = True

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


# TODO: сделать дополнительный параметр, чтобы функция могла принимать объект message из бота и выводить всю нужную инфу
def print_debug(message):
    if IS_DEBUG:
        print(message)


def db_query(query: str) -> list:
    """Выполняет любой запрос к БД, вернет полученное из неё значение"""

    try:
        with connect(
                host=bot_token.DB_HOST,
                user=bot_token.DB_USER,
                password=bot_token.DB_PWD,
                database=bot_token.DB_NAME,
        ) as connection:
            # print_debug(connection)
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                return result
    except Error as e:
        print(e)
        return []


def db_get_user_f_word_count(user_id: str) -> int:
    """Возвращает количество матов, использованных пользователем с указанным id."""

    count = db_query(f"SELECT COUNT(*) FROM fuck_facts WHERE user_id = {user_id}")
    # print_debug(f"user score = {count[0][0]}")
    if not count:
        return 0
    else:
        return count[0][0]


def db_add_f_message(f_word: str, message: telebot.types.Message) -> None:
    """Добавляет _матерное_ сообщение в БД. Использовать только для сообщений с матами. Ничего не возвращает."""

    insert_f_message = f"""
    INSERT INTO fuck_facts (user_id, user_first_name, user_last_name, username, f_word, f_message)
    VALUES
        ({message.from_user.id}, "{message.from_user.first_name}", "{message.from_user.last_name}", 
        "{message.from_user.username}", "{f_word}", "{message.text}")
    """
    db_query(insert_f_message)


def count_f_words(message: telebot.types.Message) -> int:
    """
    Считает и попутно добавляет в БД каждое употребление матерного слова из сообщения.
    Возвращает количество матов в сообщении.
    """

    total_f_count = 0

    for f_key in f_word_aliases.keys():
        # print_debug(f"{f_key} has {len(f_word_aliases[f_key])} values")
        for f_value in f_word_aliases[f_key]:
            f_entries = re.findall(f_value, message.text.lower())
            f_value_count = len(f_entries)
            # print_debug(f"Осн форма {f_key} - вариант {f_value} : {f_value_count} entries = {f_entries}")
            total_f_count = total_f_count + f_value_count

            if total_f_count:
                # на каждое встреченное использование слова добавить строку в БД
                for f_entry in f_entries:
                    # print_debug(f"-- {f_entry} of {f_key}")
                    db_add_f_message(f_key, message)

    return total_f_count


@bot.message_handler(content_types=['text'])
def text(message):
    print_debug(datetime.now().strftime('>>> %d %b %Y %H:%M (') + str(message.chat.type) + " "
                + str(message.chat.id) + "): " + message.text)

    f_count = count_f_words(message)

    if f_count:
        print_debug(f">>> f_count = {f_count}")
        bot.reply_to(message, f"{f_count} мата дектед. Алярм!\n\n"
                              f"Ваш счёт: <b>{db_get_user_f_word_count(message.from_user.id)}</b>", parse_mode="HTML")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
