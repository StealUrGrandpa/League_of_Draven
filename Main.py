import asyncio
import json
import logging
import multiprocessing
import tracemalloc
from io import BytesIO
from random import random
from runes import rune_build
import requests
from telegram import Update, Bot, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, \
    MessageHandler, filters, CallbackQueryHandler
import os
from assets.message_data_enc import decrypt_json, encrypt_json, delete_value
from flask import Flask
bot_token = os.getenv('bot_token')
bot = Bot(bot_token)

response = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
versions = response.json()
version = versions[0]


def load_key():
    secret = os.getenv('secret_key')  # Ensure the variable name matches
    if secret is None:
        raise ValueError("Environment variable SECRET_KEY is not set.")
    return secret.encode()  # Convert to bytes


def get_champion_detailed_info(champion_key):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ru_RU/champion/{champion_key}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data'][champion_key]
    return None


def get_splash(champs):
    key = get_champion_detailed_info(champs)
    keyy = key['key']

    don = f"https://cdn.communitydragon.org/{version}/champion/{keyy}/splash-art"

    return don


champ_class = {
    'Tank': 'Танк',
    'Support': 'Поддержка',
    'Marksman': 'Стрелок',
    'Mage': 'Маг',
    'Fighter': 'Воин',
    'Assassin': 'Убийца'
}

champions_data = {}

# Fetch champion data once at the start of the bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def fetch_champion_data():
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ru_RU/champion.json"
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


async def is_subscribed(user_id):
    """Check if a user is subscribed to the channel."""
    try:
        member = await bot.get_chat_member('@leagueofdravens', user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False


async def send_image(chat_id, image_url, caption, name, key, message_id):
    sub = await is_subscribed(chat_id)

    if key == 'runes':
        dict_enc = decrypt_json(load_key())
        info = dict_enc[str(chat_id)]
        name_enc = info[str(message_id)]
        print('got the data')
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Назад⬅️", "callback_data": f"backtobuilds0{name_enc}"},
                ],
            ]
        }

        reply_markup = json.dumps(keyboard)
        image, image_id = rune_build(name_enc)
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
            message_idd = result['result']['message_id']
            delete_message_url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
            delete_data = {
                "chat_id": chat_id,
                "message_id": message_idd
            }

            requests.post(delete_message_url, data=delete_data)

        file_id = image_cashe[image_id]
        data = {
            "chat_id": chat_id,
            'message_id': message_id,
            "caption": "Вот твои руны",
            "media": json.dumps({"type": "photo", "media": file_id}),
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"
        response = requests.post(send_photo_url, data=data)
        result = response.json()
        print(result)
        return result

    elif key == 'start':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Искать Чемпиона🔍", "switch_inline_query_current_chat": ""},
                ],
            ]
        }
        reply_markup = json.dumps(keyboard)
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

    elif key == 'backtobuilds':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Руны🔹", "callback_data": f"runes0{name}"},
                    {"text": "Предметы💰", "callback_data": f"items0{name}"},
                    {"text": "Назад⬅️", "callback_data": f"back0{name}"},
                ],
            ]
        }
        reply_markup = json.dumps(keyboard)
        data = {
            "chat_id": chat_id,
            'message_id': message_id,
            "caption": caption,
            "media": {
                "type": "photo",  # Указываем тип
                "media": image_url,  # URL изображения
                "caption": "Выбирай, что хочешь! 💡✨ Однако, возможно, тебе придется подождать несколько секунд, "
                           "пока билды загрузятся... ⏳ !Не нажимай по 100 раз, просто подожди!" if sub else "Выбирай, что хочешь! 💡✨ Однако, "
                                                                                                            "возможно, тебе придется подождать "
                                                                                                            "несколько секунд, пока билды "
                                                                                                            "загрузятся... ⏳ !Не нажимай по 100 раз, просто подожди! \n\n*Подпишись на "
                                                                                                            "канал, чтобы следить за "
                                                                                                            "обновлениями, и общаться с "
                                                                                                            "другими игроками!📲 "
                                                                                                            "@leagueofdravens* (Исчезнет после подписки)",
                # Подпись для изображения
                "parse_mode": "Markdown"  # Форматирование
            },
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"

        response = requests.post(send_photo_url, json=data)
        result = response.json()

    elif key == 'back':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Билды🛠️", "callback_data": f'builds0{name}'},
                    {"text": "Образы👑", "callback_data": f"skins0{name}"}
                ],

            ]
        }
        reply_markup = json.dumps(keyboard)
        print('back pressed')

        data = {
            "chat_id": chat_id,
            "caption": caption,
            "message_id": message_id,
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        send_photo_url = f"https://api.telegram.org/bot{bot_token}/editMessageCaption"
        response = requests.post(send_photo_url, data=data)
        result = response.json()

    elif key == 'query':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Билды🛠️", "callback_data": f'builds0{name}'},
                    {"text": "Образы👑", "callback_data": f"skins0{name}"}
                ],

            ]
        }
        reply_markup = json.dumps(keyboard)

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

        message_id = result["result"]["message_id"]
        secret_key = load_key()
        see = decrypt_json(secret_key)
        user_id = str(chat_id)
        MAX_MESSAGES = 100

        if user_id not in see:
            print('chat_id not in see')
            see[user_id] = {}

        if message_id not in see[user_id]:

            see[user_id][message_id] = name

            if len(see[user_id]) > MAX_MESSAGES:
                oldest_message_id = next(iter(see[user_id]))
                delete_value(user_id, message_id, secret_key)
                del see[user_id][oldest_message_id]

                # Encrypt updated dictionary
            encrypt_json(data=see, secret_key=secret_key)

            print('data saved')

    elif key == 'builds':
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Руны🔹", "callback_data": f"runes0{name}"},
                    {"text": "Предметы💰", "callback_data": f"items0{name}"},
                    {"text": "Назад⬅️", "callback_data": f"back0{name}"},
                ],
            ]
        }
        reply_markup = json.dumps(keyboard)

        data = {
            "chat_id": chat_id,
            "caption": "Выбирай, что хочешь! 💡✨ Однако, возможно, тебе придется подождать несколько секунд, "
                       "пока билды загрузятся... ⏳ !Не нажимай по 100 раз, просто подожди!" if sub else "Выбирай, что хочешь! 💡✨ Однако, "
                                                                                                        "возможно, тебе придется подождать "
                                                                                                        "несколько секунд, пока билды "
                                                                                                        "загрузятся... ⏳ !Не нажимай по 100 раз, просто подожди! \n\n*Подпишись на "
                                                                                                        "канал, чтобы следить за "
                                                                                                        "обновлениями, и общаться с "
                                                                                                        "другими игроками!📲 "
                                                                                                        "@leagueofdravens* (Исчезнет после подписки)",
            "message_id": message_id,
            "parse_mode": "Markdown",  # Use HTML parse mode
            "reply_markup": reply_markup  # Inline keyboard as a JSON string
        }
        url = f"https://api.telegram.org/bot{bot_token}/editMessageCaption"
        response = requests.post(url, data=data)
        result = response.json()
    return result


async def button_handler(update, context):
    callback_data = update.callback_query.data
    message_id = update.callback_query.message.message_id
    chat_id = update.callback_query.message.chat_id
    index_of_zero = callback_data.find('0')
    dict_enc = decrypt_json(load_key())
    info = dict_enc[str(chat_id)]
    name = info[str(message_id)]

    keyy = callback_data[:index_of_zero]

    data = get_champion_detailed_info(name)

    blurb = data["blurb"]
    title = data["id"]
    clas = ""
    for g in champions_data[name]['tags']:
        clas += str(champ_class.get(g)) + ", "
    sub = await is_subscribed(chat_id)

    if callback_data.startswith("runes"):
        print('runes')
        await bot.answer_callback_query(callback_query_id=update.callback_query.id, text="Генерирую...")
        await send_image(update.effective_chat.id, name=name, key='runes', image_url='', caption=f'{name}',
                         message_id=message_id)

    elif callback_data.startswith("items"):
        await bot.answer_callback_query(callback_query_id=update.callback_query.id, text="В разработке")

    elif callback_data.startswith("builds"):
        await send_image(update.effective_chat.id, name=name, key='builds', image_url='', caption='mamka tvoya',
                         message_id=message_id)

    elif keyy == "back" or keyy == "backtobuilds":

        rr = get_splash(title)
        message = f"*{name.title()}* ({name.title()}) \n\n*Лор*💬: {blurb}\n\n*Класс*🏆: {clas[:-2]}"
        if not sub:
            message += "\n\n*Подпишись на канал, чтобы следить за обновлениями, и общаться с другими игроками!📲 @leagueofdravens* (Исчезнет после подписки)"

        await send_image(chat_id, f"{rr}", caption=message, name=name, key=keyy, message_id=message_id)

    elif keyy == "skins":
        await bot.answer_callback_query(callback_query_id=update.callback_query.id, text="В разработке")

    else:
        print('unrecognized button')


async def start(update, context):
    await send_image(update.effective_chat.id, "https://i.ibb.co/K7JQv2w/League-of-Draven.png",
                     "Добро пожаловать в <strong>Лигу Дрейвена</strong>🏆, где всё вращается вокруг величия, славы и... Дрейвена, конечно же!🎯"
                     "\n \n Хочешь узнать что-то о чемпионах? Легко! Просто напиши <strong>@League_Of_Draven_Bot {имя чемпиона}</strong> или нажми на кнопку ниже, и я расскажу тебе всё, что ты захочешь.📜✨"
                     "\n\n Канал админа: https://t.me/leagueofdravens 📲 (Там ты сможешь следить за разработкой бота, давать свои идеи, и просто общаться)",
                     key='start', name='Draven', message_id=update.message.message_id)


async def inline_query(update: Update, context):
    results = []
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
                        thumbnail_url=f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_name}.png"
                    )
                )

    await update.inline_query.answer(results, cache_time=1)


async def chosen_inline_result(update, context):
    chosen_result1 = update.chosen_inline_result
    result_id4 = chosen_result1.result_id[:chosen_result1.result_id.index("0")]
    user_id = chosen_result1.from_user.id

    title = champions_data[result_id4]['id']
    name = champions_data[result_id4]['name']
    blurb = champions_data[result_id4]['blurb']

    clas = ""
    sub = await is_subscribed(user_id)
    for g in champions_data[result_id4]['tags']:
        clas += str(champ_class.get(g)) + ", "

    rr = get_splash(title)
    message = f"*{name.title()}* ({title.title()}) \n\n*Лор*💬: {blurb}\n\n*Класс*🏆: {clas[:-2]}"
    if not sub:
        message += "\n\n*Подпишись на канал, чтобы следить за обновлениями, и общаться с другими игроками!📲 @leagueofdravens* (Исчезнет после подписки)"

    await send_image(user_id, f"{rr}", caption=message, name=title, key='query', message_id=3245626)


async def initialize_bot():
    print("Загрузка данных о чемпионах...")
    await fetch_champion_data()
    print("Данные о чемпионах загружены.")




app = Flask(__name__)


@app.route('/')
def home():
    return "Добро пожаловать! Flask сервер работает."


def run_telegram_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())  # Устанавливаем новый событийный цикл для этого потока
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_bot())  # Инициализируем бота асинхронно

    application = ApplicationBuilder().token(bot_token).build()

    tracemalloc.start()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(ChosenInlineResultHandler(chosen_inline_result))

    application.run_polling()


# Main function
def run_flask():
    app.run(host='0.0.0.0', port=8000)
    print("Flask сервер работает.")


if __name__ == "__main__":
    t1 = multiprocessing.Process(target=run_flask)
    t2 = multiprocessing.Process(target=run_telegram_bot)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
