import db_setup
import telebot
from mysql.connector import connect, Error


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
    """Возвращает количество матов, использованных пользователем с указанным id, в указанном чате"""

    if chat_id=="*":
        count = db_query(f"SELECT COUNT(*) FROM fuck_facts WHERE user_id = {user_id}")
    else:
        count = db_query(f"SELECT COUNT(*) FROM fuck_facts WHERE user_id = {user_id} AND chat_id = {chat_id}")

    if not count:
        return 0
    else:
        return count[0][0]


def db_get_users_score_table(chat_id="*") -> str:
    """Выдает рейтинг пользователей в чате chat_id. Без параметра выдает сквозной рейтинг по всем чатам."""

    if not chat_id=="*":
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
    users_score_table = ""

    for row in query_result:
        if str(row[3]) == "None":
            username = " "
        else:
            username = f"@{str(row[3])}"

        if str(row[5]) == "None":
            last_name = " "
        else:
            last_name = f"{str(row[5])}"

        users_score_table = f"{users_score_table}{str(row[1])} - {username} {row[4]} {last_name}\n"

    return users_score_table


def db_add_f_message(f_word: str, message: telebot.types.Message) -> None:
    """Добавляет _матерное_ сообщение в БД. Использовать только для сообщений с матами. Ничего не возвращает."""

    insert_f_message = f"""
    INSERT INTO fuck_facts (user_id, chat_id, user_first_name, user_last_name, username, f_word, f_message)
    VALUES
        ("{message.from_user.id}", "{str(message.chat.id)}", "{message.from_user.first_name}", "{message.from_user.last_name}", 
        "{message.from_user.username}", "{f_word}", "{message.text}")
    """
    db_query(insert_f_message)
