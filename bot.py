import time

import requests
import json
import telebot

# Замените 'YOUR_TOKEN' на токен вашего бота
API_TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def get_mp4_links(message):
    try:
        # Преобразуем текст сообщения в число
        number = int(message.text)

        url = "https://apiv2.tik.porn/getnextvideos"

        headers = {
            "accept": "application/json",
            "accept-language": "ru-RU,ru;q=0.9",
            "content-type": "application/json",
            "origin": "https://tik.porn",
            "priority": "u=1, i",
            "referer": "https://tik.porn/",
        }

        data = {
            "amount": number,
            "filters": [463387, 626753, 626767, 615056],  # Здесь можно изменить другие фильтры, я выбрал пару виосов которые нравятся большинству
        }

        # Выполнение POST-запроса
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = response.json()

            # Извлечение mp4_url
            mp4_urls = [video["mp4_url"] for video in response_data.get('data', []) if "mp4_url" in video]

            # Отправка ссылок в ответ, исключая определенную ссылку
            for url in mp4_urls:
                bot.send_video(message.chat.id, url)
                time.sleep(1.5)
                print(url)
        else:
            bot.send_message(message.chat.id, f"Ошибка {response.status_code}: {response.text}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите допустимое число.")


# Запуск бота
bot.polling(none_stop=True)
