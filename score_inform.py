import bot_utils
import db_utils

#  TODO: ПЕРЕД ЗАПУСКОМ ВЫБРАТЬ BOT_CHAT_ID и TOKEN в bot_token.py !!!
BOT_CHAT_ID = "133637887"  # DebugBot chat with me
# BOT_CHAT_ID = "-1001594961681"  # Пацантрэ
# BOT_CHAT_ID = "-1001726929655"  # MTG

score_table = db_utils.db_get_users_score_table()

bot_utils.print_debug(score_table)
bot_utils.bot_sendtext(BOT_CHAT_ID, f"<b>Поприветствуем ударников матерного фронта:</b>\n\n{score_table}")
