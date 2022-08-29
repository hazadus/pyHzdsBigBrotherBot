# pyHzdsBigBrotherBot
Тестовый Telegram-бот для тестирования и отладки разных фишек.
В настоящее время мониторит все сообщения на предмет
использования ненормативной лексики, считает количество
употребления каждого слова по каждому пользователю для составления
рейтинга матершинников и самых популярных матерных слов.

## Dependencies
- `pytelegrambotapi`
- `mysql-connector-python`

## Installation
- Создать файл `bot_token.py` с переменной `TOKEN`, содержащей
token бота.
- Создать файл `db_setup.py` с настройками БД MySQL.
- Создать необходимые таблицы в БД.

## Upcoming features
- [Issues on GitHub](https://github.com/hazadus/pyHzdsBigBrotherBot/issues)