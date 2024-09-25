import requests
import os
import logging
import time

from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)

token = os.getenv('TOKEN')
bot = TeleBot(token=token)

URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
        response.raise_for_status()
        logging.info("Используем альтернативный API для получения изображения собачки.")
        print("Извините, мы уже чиним картинки с котиками, вот вам пока картинка с собачкой.")

    response = response.json()
    random_cat = response[0].get('url')
    logging.info(f'Получено изображение котика: {random_cat}')
    return random_cat


def get_new_kitten_image():
    url = 'https://cataas.com/cat/kitten?position=center'
    headers = {
        'accept': 'image/*'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info('Изображение котенка успешно получено.')
        return response.content
    except Exception as error:
        logging.error(f'Ошибка при получении изображения котенка: {error}')
        return None


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    try:
        cat_image_url = get_new_image()
        bot.send_photo(chat.id, cat_image_url)
        logging.info(f'Отправлено изображение котика в чат {chat.id}.')
    except Exception as error:
        logging.error(f'Ошибка при отправке изображения котика: {error}')


@bot.message_handler(commands=['kitten'])
def send_kitten(message):
    chat = message.chat
    kitten_image = get_new_kitten_image()

    if kitten_image:
        bot.send_photo(chat.id, kitten_image)
        logging.info(f'Отправлено изображение котенка в чат {chat.id}.')
    else:
        bot.send_message(chat.id, "Извините, не удалось получить изображение котенка.")
        logging.warning(f'Не удалось получить изображение котенка для чата {chat.id}.')


@bot.message_handler(commands=['gif'])
def send_new_kitten_gif(message):
    url = f'https://cataas.com/cat/gif?position=center&rand={time.time()}'

    try:
        response = requests.get(url, headers={'accept': 'image/*'})
        chat = message.chat

        if response.status_code == 200:
            bot.send_animation(chat.id, response.url)
            logging.info(f'Отправлена гифка котика в чат {chat.id}.')
        else:
            bot.send_message(chat.id, "Извините, не удалось получить изображение котенка.")
            logging.warning(f'Ошибка получения гифки для чата {chat.id}: статус {response.status_code}')
    except Exception as error:
        logging.error(f'Ошибка при отправке гифки: {error}')


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    # Создаём объект клавиатуры:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаём объект кнопки:
    button_newcat = types.KeyboardButton('/newcat')
    button_kitten = types.KeyboardButton('/kitten')
    button_gif = types.KeyboardButton('/gif')
    # Добавляем объекты кнопок на клавиатуру:
    keyboard.add(button_newcat, button_kitten,button_gif)

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