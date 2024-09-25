import requests
import os
import logging

from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

token = os.getenv('TOKEN')

bot = TeleBot(token=token)



URL = 'https://api.thecatapi.com/v1/images/search'

# Код запроса к thecatapi.com и обработку ответа обернём в функцию:
def get_new_image():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
        response.raise_for_status()
        print("Извините, мы уже чиним картинки с котиками, вот вам пока картинка с собачкой.")

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_new_kitten_image():
    url = 'https://cataas.com/cat/kitten?position=center'
    headers = {
        'accept': 'image/*'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f'Ошибка: {response.status_code}')
        return None

def get_new_cat_gif():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
        response.raise_for_status()
        print("Извините, мы уже чиним картинки с котиками, вот вам пока картинка с собачкой.")

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


# Добавляем хендлер для команды /newcat:
@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())

@bot.message_handler(commands=['kitten'])
def send_kitten(message):
    chat = message.chat
    kitten_image = get_new_kitten_image()  # Получаем изображение котенка

    if kitten_image:
        # Отправляем изображение котенка
        bot.send_photo(chat.id, kitten_image)
    else:
        # Если не удалось получить изображение, отправляем сообщение об ошибке
        bot.send_message(chat.id, "Извините, не удалось получить изображение котенка.")




@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    # Создаём объект клавиатуры:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаём объект кнопки:
    button_newcat = types.KeyboardButton('/newcat')
    button_kitten = types.KeyboardButton('/kitten')
    # Добавляем объекты кнопок на клавиатуру:
    keyboard.add(button_newcat, button_kitten)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        reply_markup=keyboard,
    )

    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()