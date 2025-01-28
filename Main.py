import asyncio
import json
import logging
import tracemalloc
from io import BytesIO
from random import random
from runes import rune_build
import requests
from telegram import Update, Bot, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, \
    MessageHandler, filters, CallbackQueryHandler

import os

bot_token = os.getenv('bot_token')

def reworked_chams(champs):

    url = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/data/ru_RU/champion.json"

    response = requests.get(url)
    response.raise_for_status()
    data1 = response.json()

    key = data1.get("data", {}).get(champs, {}).get("key")

    ro = key + "/" + key + "000"

    don = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-splashes/{ro}.jpg"

    return don


champ_class = {
    'Tank': 'Танк',
    'Support': 'Поддержка',
    'Marksman': 'Стрелок',
    'Mage': 'Маг',
    'Fighter': 'Воин',
    'Assassin': 'Убийца'
}

chams = ["Pantheon", "DrMundo", "Jax", "Sivir", "Hecarim", "Kassadin", "Volibear", "Udyr", 'Morgana']
champions_data = {}

# Fetch champion data once at the start of the bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot = Bot(bot_token)


def get_champion_detailed_info(champion_key):
    url = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/data/ru_RU/champion/{champion_key}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data'][champion_key]
    return None
async def recent_message():
    get_updates_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    response = requests.get(get_updates_url)
    updates = response.json()

    if updates["ok"] and updates["result"]:
        latest_message = updates["result"][-1]
        return latest_message["message"]["message_id"]
    else:
        return None

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

    await bot.delete_message(chat_id=user_id, message_id=message.message_id)

image_cashe = {}
async def send_image(chat_id, image_url, caption, name, key):
    global name_global
    global last_message_id
    if key == 'query' or key == 'back':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Билды🛠️", "callback_data": f'builds0{name}'},
                    {"text": "Образы👑", "callback_data": f"skins0{name}"}
                ],

            ]
        }
    elif key == 'builds' or key == 'backtobuilds':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Руны🔹", "callback_data": f"runes0{name}"},
                    {"text": "Предметы💰", "callback_data": f"items0{name}"},
                    {"text": "Назад⬅️", "callback_data": f"back0{name}" },
                ],
            ]
        }
    elif key == 'runes' or key == 'items':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Назад⬅️", "callback_data": f"backtobuilds0{name}"},
                ],
            ]
        }
    elif key == 'start':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Искать Чемпиона🔍", "switch_inline_query_current_chat": ""},
                ],
            ]
        }
    reply_markup = json.dumps(keyboard)

    if key == 'runes':
        image, image_id = rune_build(name)
        if image_id not in image_cashe.keys():
            print(str(image_id) + "not found")

            img_buffer = BytesIO()
            image.save(img_buffer, format="PNG")
            img_buffer.seek(0)  # Move to the beginning of the buffer

            # Set caption and delete the previous message
            send_photo_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            data = {
                "chat_id": chat_id,
                "caption": caption,
                "parse_mode": "Markdown",
                "reply_markup": reply_markup
            }
            files = {"photo": ("image.png", img_buffer, "image/png")}
            response = requests.post(send_photo_url, data=data, files=files)
            result = response.json()

            # Extract file_id from the response
            file_id = result['result']['photo'][0]['file_id']
            image_cashe[image_id] = file_id
            print(str(image_id) + "saved")
            message_id = result['result']['message_id']
            delete_message_url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
            delete_data = {
                "chat_id": chat_id,
                "message_id": message_id
            }

            requests.post(delete_message_url, data=delete_data)



        file_id = image_cashe[image_id]
        data = {
            "chat_id": chat_id,
            'message_id': last_message_id,
            "caption": "Вот твои руны",
            "media": json.dumps({"type": "photo", "media": file_id}),
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"
        response = requests.post(send_photo_url, data=data)
        result = response.json()
        return result

    elif key == 'start':
        data = {
            "chat_id": chat_id,
            "caption": caption,
            'photo': image_url,
            "parse_mode": "HTML",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        response = requests.post(send_photo_url, data=data)
        result = response.json()
        print(result)
        return result

    elif key == 'backtobuilds':
        data = {
            "chat_id": chat_id,
            'message_id': last_message_id,
            "caption": caption,
            "media": {
                    "type": "photo",  # Указываем тип
                    "media": image_url,  # URL изображения
                    "caption": 'Выбирай, что хочешь! 💡✨ Однако, возможно, тебе придется подождать несколько секунд, пока билды загрузятся... ⏳',  # Подпись для изображения
                    "parse_mode": "Markdown"  # Форматирование
            },
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"

        response = requests.post(send_photo_url, json=data)
        result = response.json()



        return result

    elif key == 'back':
        print('back pressed')

        data = {
            "chat_id": chat_id,
            "caption": caption,
            "message_id": last_message_id,
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/editMessageCaption"
        response = requests.post(send_photo_url, data=data)
        result = response.json()


        return result

    elif key == 'query':
        print('got it here')
        data = {
            "chat_id": chat_id,
            "caption": caption,
            'photo': image_url,
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        response = requests.post(send_photo_url, data=data)
        result = response.json()


        return result
    elif key == 'builds':
        print('builds')
        data = {
            "chat_id": chat_id,
            "caption": "Выбирай, что хочешь! 💡✨ Однако, возможно, тебе придется подождать несколько секунд, пока билды загрузятся... ⏳",
            "message_id": last_message_id,
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        print(str(last_message_id) + "builds")
        url = f"https://api.telegram.org/bot{bot_token}/editMessageCaption"
        response = requests.post(url, data=data)
        result = response.json()

        return result




async def button_handler(update, context):
    global name_global
    global query_info
    chat_id = query_info['result']['chat']['id']
    global last_message_id
    callback_data = update.callback_query.data
    index_of_zero = callback_data.find('0')
    name = callback_data[index_of_zero + 1:]
    keyy = callback_data[:index_of_zero]

    if not name:
        name = name_global


    if callback_data.startswith("runes"):
        print('runes')
        await send_image(update.effective_chat.id, name=name, key='runes', image_url='', caption=f'{name}')

    elif callback_data.startswith("items"):
        await bot.answer_callback_query(callback_query_id=update.callback_query.id, text="В разработке")

    elif callback_data.startswith("builds"):
        await send_image(update.effective_chat.id, name=name, key='builds', image_url='',caption='mamka tvoya')

    elif keyy == "back" or keyy == "backtobuilds":
        if name in chams:
            rr = reworked_chams(name)

        else:
            rr = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{name}_0.jpg"
        await send_image(chat_id, rr, query_info['result']['caption'], name='', key=keyy)

    elif keyy == "skins":
        await bot.answer_callback_query(callback_query_id=update.callback_query.id, text="В разработке")


async def start(update, context):
    await send_image(update.effective_chat.id, "https://i.ibb.co/K7JQv2w/League-of-Draven.png",
                     "Добро пожаловать в <strong>Лигу Дрейвена</strong>🏆, где всё вращается вокруг величия, славы и... Дрейвена, конечно же!🎯"
                     "\n \n Хочешь узнать что-то о чемпионах? Легко! Просто напиши <strong>@League_Of_Draven_Bot {имя чемпиона}</strong> или нажми на кнопку ниже, и я расскажу тебе всё, что ты захочешь.📜✨"
                     "\n\n Канал админа: https://t.me/leagueofdravens 📲 (Там ты сможешь следить за разработкой бота, давать свои идеи, и просто общаться)", key='start', name='Draven')





async def inline_query(update: Update, context):
    results = []
    global name_global
    query = update.inline_query.query
    if query:
        for champion_name, data in champions_data.items():
            name = data.get("name", "")
            if name.lower().startswith(query.lower()):
                results.append(
                    InlineQueryResultArticle(
                        id=champion_name + str(random()),
                        title=name.title(),
                        description=data.get("title", ""),
                        input_message_content=InputTextMessageContent(f'Нашел!: {name.title()}'),
                        thumbnail_url=f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champion_name}.png"
                    )
                )

    await update.inline_query.answer(results, cache_time=1)


async def chosen_inline_result(update, context):
    print("chosen_inline_result triggered")
    global name_global
    global last_message_id
    global query_info
    chosen_result1 = update.chosen_inline_result
    result_id4 = chosen_result1.result_id[:chosen_result1.result_id.index("0")]
    user_id = chosen_result1.from_user.id
    title = champions_data[result_id4]['id']
    name = champions_data[result_id4]['name']
    blurb = champions_data[result_id4]['blurb']
    name_global = title
    clas = ""
    for g in champions_data[result_id4]['tags']:
        clas += str(champ_class.get(g)) + ", "

    if title in chams:
        rr = reworked_chams(title)

    else:
        rr = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{title}_0.jpg"

    sent_message = await send_image(user_id, f"{rr}", f"*{name.title()}* \n\n*Лор*💬: {blurb}\n\n*Класс*🏆: {clas[:-2]}", name=title, key='query')

    last_message_id = sent_message['result']['message_id']
    query_info = sent_message



async def initialize_bot():
    print("Загрузка данных о чемпионах...")
    await fetch_champion_data()
    print("Данные о чемпионах загружены.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_bot())
    application = ApplicationBuilder().token(bot_token).build()

    tracemalloc.start()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CallbackQueryHandler(button_handler))  # Register the callback query handler for inline buttons
    application.add_handler(ChosenInlineResultHandler(chosen_inline_result))

    application.run_polling()
