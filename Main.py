import asyncio
import logging
from asyncio import create_task
from random import randint, random
from time import time
from asyncio import create_task, sleep, CancelledError
from uuid import uuid4
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, Bot, InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, \
    MessageHandler, filters

from Dictionaries import reworked_chams, champ_class, letter_to_number, champions_by_letter, get_tags, ru_to_en, find_letter

chams = ["Pantheon", "DrMundo", "Jax", "Sivir", "Hecarim", "Kassadin", "Volibear, Udyr"]
champions_data = {}
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot = Bot("7052706701:AAHo9_cEwYowA8DeQOW9ghPTtPMNkl-3khE")

async def fetch_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/14.24.1/data/ru_RU/champion.json"
    response = requests.get(url)
    if response.status_code == 200:
        champions_data.update(response.json()['data'])
    else:
        print("Ошибка загрузки данных о чемпионах.")

async def message_handler(update, context):
    message = update.message
    user_id = message.from_user.id
    user_name = message.from_user.username
    text = message.text
    print(message.message_id)
    print(f"Received message from user {user_name} (ID: {user_id}): {text}")
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)


import requests
import json


async def send_image(chat_id, image_url, caption, ):
    # Define the inline keyboard buttons
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Button 1", "callback_data": "button1"},
                {"text": "Button 2", "callback_data": "button2"}
            ],
            [
                {"text": "Visit Website", "url": "https://example.com"}
            ]
        ]
    }

    # Convert the keyboard to a JSON string
    reply_markup = json.dumps(keyboard)

    send_photo_url = "https://api.telegram.org/bot7052706701:AAHo9_cEwYowA8DeQOW9ghPTtPMNkl-3khE/sendPhoto"

    # Prepare the data payload
    data = {
        "chat_id": chat_id,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "HTML",  # Use HTML parse mode
        "reply_markup": reply_markup  # Inline keyboard as a JSON string
    }

    # Send the POST request
    response = requests.post(send_photo_url, data=data)

    # Parse the response
    result = response.json()

    if response.status_code == 200 and result.get('ok'):
        print('norm vse')  # Success
        return result
    else:
        print('gavno')  # Failure
        print(f"Error: {result.get('description', 'Unknown error')}")
        return {"error": result.get('description', 'Unknown error'), "status_code": response.status_code}


async def start(update, context):
    await send_image(update.effective_chat.id, "https://i.ibb.co/K7JQv2w/League-of-Draven.png",
                     "Добро пожаловать в Лигу Дрейвена, где всё вращается вокруг величия, славы и... Дрейвена, конечно же! "
                     "\n \n Хочешь узнать о чемпионах? Легко! Просто напиши @League_Of_Draven_Bot {имя чемпиона}, и я расскажу тебе всё, что ты захочешь."
                     "\n\n Канал админа: https://t.me/leagueofdravens")


def get_champion_detailed_info(champion_key):
    url = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/data/ru_RU/champion/{champion_key}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data'][champion_key]
    return None


async def inline_query(update: Update, context):

    results = []
    query = update.inline_query.query
    if query:
        for champion_name, data in champions_data.items():
            name = data.get("name", "")
            if data.get('name').lower().startswith(query.lower()):
                blurb = data.get("blurb", "")
                clas = ""
                for g in data.get("tags", ""):
                    print(g)
                    clas += str(champ_class.get(g)) + ", "

                print(data.get("name", "").lower())
                localized_name = data.get("name", "").lower()  # Get the Russian name of the champion
                if localized_name.startswith(query):
                    # Fetch additional data like "blurb"
                    if champion_name in chams:
                        dd = reworked_chams(champion_name)
                    else:
                        dd = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_name}_0.jpg"


                    # Add result to the inline query
                    results.append(
                        InlineQueryResultArticle(
                            id=champion_name + str(random()),
                            title=name.title(),
                            input_message_content=InputTextMessageContent(
                                f"*{name.title()}* \n\n*Лор*💬: {blurb}\n\nКласс: {clas}\n\n{dd}"

                            ),
                            thumbnail_url=f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champion_name}.png"
                        )
                    )
                    print('yep')
            else:
                print('nope')

    await update.inline_query.answer(results, cache_time=1)

async def chosen_inline_result(update, context):
    chosen_result1 = update.chosen_inline_result
    result_id4 = chosen_result1.result_id[:chosen_result1.result_id.index("0")]
    user_id = chosen_result1.from_user.id
    message = update.message.text
    print(f"Chosen inline result: {chosen_result1.result_id}")

    if result_id4 in chams:
        rr = reworked_chams(result_id4)

    else:
        rr = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{result_id4}_0.jpg"


    await send_image(user_id, f"{rr}", f"*{message}")



async def initialize_bot():
    print("Загрузка данных о чемпионах...")
    await fetch_champion_data()
    print("Данные о чемпионах загружены.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_bot())
    application = ApplicationBuilder().token('7052706701:AAHo9_cEwYowA8DeQOW9ghPTtPMNkl-3khE').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    application.add_handler(InlineQueryHandler(inline_query))

    application.add_handler(ChosenInlineResultHandler(chosen_inline_result))

    application.run_polling()
