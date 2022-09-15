# API docs: https://openweathermap.org/api
# Weather in St. Petersburg https://openweathermap.org/city/498817
import requests as req

import api_keys
import bot_utils

# BOT_CHAT_ID = "133637887"  # DebugBot chat with me
BOT_CHAT_ID = "-1001594961681"  # Пацантрэ
# BOT_CHAT_ID = "-1001726929655"  # MTG


def get_weather_html() -> str:
    loc = 'St. Petersburg'
    api_url = "https://api.openweathermap.org/data/2.5/weather?"
    params = f"q={loc}&lang=ru&appid={api_keys.API_KEY_OPENWEATHER}"

    # Get the response from the API
    url = api_url + params
    response = req.get(url)
    # TODO: check response before continuing

    weather = response.json()
    weather_html = "<b>Погода в Санкт-Петербурге:</b>\n\n"

    # Fetch Weather
    temp = weather['main']['temp']
    weather_html += "Температура: " + "{:.1f}".format(temp - 273.15) + " °C, "\
                    + weather['weather'][0]['description'] + "\n"

    humidity = weather['main']['humidity']
    weather_html += "Влажность: " + str(humidity) + "%\n"

    wind = weather['wind']['speed']
    weather_html += "Ветер: " + str(wind) + " м/с"

    return weather_html


# main
if __name__ == "__main__":
    bot_utils.bot_sendtext(BOT_CHAT_ID, get_weather_html())
