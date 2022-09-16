from mysql.connector import connect, Error

import db_setup
import telebot


def db_query(query: str) -> list:
    """Выполняет любой запрос к БД, вернет полученное из неё значение"""

    try:
        with connect(
                host=db_setup.DB_HOST,
                user=db_setup.DB_USER,
                password=db_setup.DB_PWD,
                database=db_setup.DB_NAME,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                return result
    except Error as e:
        print(e)
        return []


def db_get_user_f_word_count(user_id: str, chat_id="*") -> int:
    """Возвращает количество матов, использованных пользователем с указанным id, в указанном чате, либо во всех чатах,
    если chat_id не указан."""

    if chat_id == "*":
        count = db_query(f"SELECT COUNT(*) FROM fuck_facts WHERE user_id = {user_id}")
    else:
        count = db_query(f"SELECT COUNT(*) FROM fuck_facts WHERE user_id = {user_id} AND chat_id = {chat_id}")

    if not count:
        return 0
    else:
        return count[0][0]


def db_get_users_score_table_html(chat_id="*") -> str:  # TODO: сделать вариант, который возвращает неформатированный список
    """Выдает рейтинг пользователей в чате chat_id в формате HTML. Без параметра выдает сквозной рейтинг
    по всем чатам."""

    if not chat_id == "*":
        query = f"""
        SELECT *
        FROM (SELECT fuck_facts.user_id, COUNT(*) FROM fuck_facts
            WHERE chat_id="{chat_id}" GROUP BY user_id ORDER BY COUNT(*) DESC) AS A
        JOIN (SELECT DISTINCT(user_id), username, user_first_name, user_last_name FROM fuck_facts
            WHERE chat_id="{chat_id}") AS B
        ON A.user_id=B.user_id    
        """
    else:
        query = f"""
        SELECT *
        FROM (SELECT fuck_facts.user_id, COUNT(*) FROM fuck_facts
            GROUP BY user_id ORDER BY COUNT(*) DESC) AS A
        JOIN (SELECT DISTINCT(user_id), username, user_first_name, user_last_name FROM fuck_facts) AS B
        ON A.user_id=B.user_id    
        """

    query_result = db_query(query)
    users_scores_html = ""

    for row in query_result:
        if str(row[3]) == "None":
            username = " "
        else:
            username = f"@{str(row[3])}"

        if str(row[5]) == "None":
            last_name = " "
        else:
            last_name = f"{str(row[5])}"

        users_scores_html = f"{users_scores_html}\U0001F5E3{str(row[1])} - {username} {row[4]} {last_name}\n"

    return users_scores_html


def db_add_f_message(f_word: str, message: telebot.types.Message) -> None:
    """Добавляет _матерное_ сообщение в БД. Использовать только для сообщений с матами. Ничего не возвращает."""

    insert_f_message = f"""
    INSERT INTO fuck_facts (user_id, chat_id, user_first_name, user_last_name, username, f_word, f_message)
    VALUES
        ("{message.from_user.id}", "{str(message.chat.id)}", "{message.from_user.first_name}", "{message.from_user.last_name}", 
        "{message.from_user.username}", "{f_word}", "{message.text}")
    """
    db_query(insert_f_message)


def db_add_any_message(message: telebot.types.Message) -> None:
    """Добавляет любое сообщение чата в отдельную таблицу (для дальнейшего её анализа"""

    insert_message = f"""
    INSERT INTO all_messages (user_id, chat_id, user_first_name, user_last_name, username, message)
    VALUES
        ("{message.from_user.id}", "{str(message.chat.id)}", "{message.from_user.first_name}", 
        "{message.from_user.last_name}",  "{message.from_user.username}", "{message.text}")
    """
    db_query(insert_message)


def db_get_f_words_rating(chat_id="*") -> list:  # TODO: сделать варик, возвращающий форматированный текст
    """Возвращает список вида [("Хуй": 58)] с рейтингом матерных слов (отсортированный по убыванию)."""

    if chat_id == "*":
        rating = db_query(f"SELECT DISTINCT(f_word), COUNT(*) FROM fuck_facts GROUP BY f_word ORDER BY COUNT(*) DESC")
    else:
        rating = db_query(f"SELECT DISTINCT(f_word), COUNT(*) FROM fuck_facts WHERE chat_id={chat_id} "
                          f"GROUP BY f_word ORDER BY COUNT(*) DESC")

    return rating


def db_get_f_words_rating_html(chat_id="*") -> str:
    """Возвращает рейтинг матерных слов, отформатированный в HTML, в чате с chat_id, или сквозной по всем чатам."""

    word_emojis = {
        "Хуй": "\U0001F346",
        "Хер": "\U0001F336",
        "Залупа": "\U0001F50E",
        "Пизда": "\U0001F351",
        "Манда": "\U0001F34A",
        "Ебать": "\U0001F4A5",
        "Блядь": "\U0001F64E",
        "Пидор": "\U0001FAC3"
    }

    f_rating_html = "<b>Рейтинг матерных слов:</b>\n"
    for row in db_get_f_words_rating(chat_id):
        f_word, score = row
        f_rating_html = f"{f_rating_html}{f_word}{word_emojis.get(f_word, '')} - {score}\n"

    return f_rating_html
