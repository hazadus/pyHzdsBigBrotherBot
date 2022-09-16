import bot_utils
import db_utils

# BOT_CHAT_ID = "133637887"  # DebugBot chat with me
BOT_CHAT_ID = "-1001594961681"  # Пацантрэ
# BOT_CHAT_ID = "-1001726929655"  # MTG

score_table = db_utils.db_get_users_score_table_html(BOT_CHAT_ID)
word_rating = db_utils.db_get_f_words_rating_html(BOT_CHAT_ID)

bot_utils.print_debug(score_table)
bot_utils.bot_sendtext(BOT_CHAT_ID, f"<b>Поприветствуем ударников матерного фронта:</b>\n\n{score_table}\n"
                                    f"{word_rating}\n"
                                    f"<i>Рейтинг по данным из этого чата</i>")
