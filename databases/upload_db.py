import json
import base64
import io
import time

from PIL import Image
import requests

from databases.database_conf import add_champion
from runes import rune_build


def upload_db(champion):
    image = rune_build(champion)
    add_champion(champion, image)
def base64_to_image(encoded_image):
    img_data = base64.b64decode(encoded_image)
    byte_io = io.BytesIO(img_data)
    image = Image.open(byte_io)
    return image

def get_image(champion, data):
    start_time = time.time()
    headers = {"Accept-Encoding": "gzip"}
    url = data
    params = {"id": champion.title()}  # Requesting only one value by ID
    response = requests.get(url, params=params, headers=headers)

    image_data = response.text

    # Convert base64 image string into an image
    decoded_image = base64_to_image(image_data)

    # Save the image as JPEG or any other format you want


    end_time = time.time()
    print("Time of getting the image and decoding: " + str(end_time - start_time))
    return decoded_image

def champion_names():
    url = "https://ddragon.leagueoflegends.com/cdn/12.20.1/data/en_US/champion.json"
    response = requests.get(url)
    data = response.json()  # Parse JSON response
    champions = data['data'].keys()  # Get the names of all champions
    return champions

def upload_all():
    names = champion_names()

    for i in names:
        print("uploading " + i)
        upload_db(i)
        print("uploaded " + i)