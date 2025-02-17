import base64
import io
import json
import random
from io import BytesIO

import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from bs4 import BeautifulSoup


def get_runes(champion):
    # URL of the webpage to scrape
    url = f"https://u.gg/lol/champions/{champion}/build"


    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    # Fetch the HTML content of the webpage
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP request errors

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract rune information
    runes = []
    seen_runes = set()  # To track already seen runes

    for perk in soup.select(".perk"):
        img = perk.find("img")
        if img:
            name = img.get("alt", "").replace("The Rune ", "").replace("The Keystone ", "")
            img_url = img.get("src")
            is_active = "perk-active" in perk.get("class", [])

            # Add the rune only if it's not already seen
            if name not in seen_runes:
                runes.append({"name": name, "image_url": img_url, "active": is_active})
                seen_runes.add(name)

    # Print the extracted rune data

    for shard in soup.select(".shard"):
        img = shard.find("img")
        if img:
            name = img.get("alt", "").replace("The ", "").replace("Shard", "").strip()
            img_url = img.get("src")
            is_active = "shard-active" in shard.get("class", [])
            runes.append({"name": name, "image_url": img_url, "active": is_active})

    # Extract the primary rune tree name (e.g., Sorcery, Domination)
    primary_tree = soup.select_one(".primary-tree .perk-style-title .pointer")
    primary_treesrc = soup.select_one(".primary-tree .rune-image-container img")
    primary_src = primary_treesrc.get("src")
    primary_tree_name = primary_tree.text.strip() if primary_tree else "Unknown"

    # Extract the secondary rune tree name
    secondary_tree = soup.select_one(".secondary-tree .perk-style-title .pointer")
    secondary_treesrc = soup.select_one(".secondary-tree .rune-image-container img")
    secondary_src = secondary_treesrc.get("src")
    secondary_tree_name = secondary_tree.text.strip() if secondary_tree else "Unknown"
    runes.append({'prime': primary_tree_name, 'prime_img': primary_src, 'secondary': secondary_tree_name,
                  'secondary_img': secondary_src})

    # Print shards
    return runes


en_to_ru = {
    'Domination': 'Доминирование',
    'Inspiration': 'Вдохновение',
    'Resolve': 'Храбрость',
    'Precision': 'Точность',
    'Sorcery': 'Колдовство'
}

image_cache = {}

def save_to_memory_cache(champion, image):
    """Save the image in memory."""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    image_cache[champion] = {
        'image': img_byte_arr.getvalue(),
        'runes': get_runes(champion),
        'image_id': random.random()
    }

def load_from_memory_cache(champion, why):

    if champion in image_cache and why == 'image':
        img_byte_arr = io.BytesIO(image_cache[champion]['image'])
        return Image.open(img_byte_arr)
    elif champion in image_cache and why == 'image_id':
        return image_cache[champion]['image_id']
    elif champion in image_cache and why == 'runes':
        return image_cache[champion]['runes']
    return None
def fetch_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# Function to generate a unique hash based on input data

def rune_build(champion):
    info = get_runes(champion=champion)
    cached_image = load_from_memory_cache(champion, 'image')
    image_id = load_from_memory_cache(champion, 'image_id')
    if cached_image and load_from_memory_cache(champion, 'runes') == info:
        return cached_image, image_id # Print cached stats
    else:


        print(f"Generating new image for {champion}")

        for i in info[-1:]:

            prime = i['prime']

            secondary = i['secondary']

            prime_img = i['prime_img']

            secondary_img = i['secondary_img']


        def big_prime():
            big_prime_imgs = []
            activity_big_prime = []
            if prime == "Precision":
                for img in info[:4]:
                    big_prime_imgs.append(fetch_image(img['image_url']))
                    activity_big_prime.append((img['active']))
            else:

                for img in info[:3]:
                    big_prime_imgs.append(fetch_image(img['image_url']))
                    activity_big_prime.append((img['active']))

            return big_prime_imgs, activity_big_prime

        def little_prime():
            little_prime_imgs = []
            activity_little_prime = []
            if prime == "Precision":
                for img in info[4:13]:
                    little_prime_imgs.append(fetch_image(img['image_url']))
                    activity_little_prime.append((img['active']))
            else:
                for img in info[3:12]:
                    little_prime_imgs.append(fetch_image(img['image_url']))
                    activity_little_prime.append((img['active']))

            return little_prime_imgs, activity_little_prime

        def big_secondary():
            big_secondary_imgs = []
            activity_big_secondary = []
            if prime == "Precision":
                for img in info[13:22]:
                    big_secondary_imgs.append(fetch_image(img['image_url']))
                    activity_big_secondary.append((img['active']))
            else:
                for img in info[12:21]:
                    big_secondary_imgs.append(fetch_image(img['image_url']))
                    activity_big_secondary.append((img['active']))

            return big_secondary_imgs, activity_big_secondary

        def little_secondary():
            little_secondary_imgs = []
            activity_little_secondary = []
            if prime == "Precision":
                for img in info[22:31]:
                    little_secondary_imgs.append(fetch_image(img['image_url']))
                    activity_little_secondary.append((img['active']))
            else:
                for img in info[21:30]:
                    little_secondary_imgs.append(fetch_image(img['image_url']))
                    activity_little_secondary.append((img['active']))

            return little_secondary_imgs, activity_little_secondary

        canvas_width = 1200
        canvas_height = 720

        # Create a blank canvas
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (67, 61, 139, 255))
        draw = ImageDraw.Draw(canvas, "RGBA")
        rectangle_bounds = [125, 50, 550, 150]
        draw.rounded_rectangle([125, 50, 550, 150], radius=30, fill=(46, 35, 108, 255))
        text = en_to_ru[prime]
        text_color = (255, 255, 255)
        font = ImageFont.truetype(r"beaufort.ttf", 50)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1] + 25

        rect_x1, rect_y1, rect_x2, rect_y2 = rectangle_bounds
        rect_width = rect_x2 - rect_x1
        rect_height = rect_y2 - rect_y1

        # Center text position
        text_x = rect_x1 + (rect_width - text_width) / 2
        text_y = rect_y1 + (rect_height - text_height) / 2

        # Draw the text
        draw.text((text_x, text_y), text, font=font, fill=text_color, align='center')
        p_img = fetch_image(prime_img)
        canvas.paste(p_img, (40, 50), mask=p_img)

        if prime == "Precision":
            x = 125

        else:
            x = 175

        def draw_rounded_background(draw, position, size, radius, color):
            # Draw a rounded rectangle as the background
            x1, y1 = position
            x2, y2 = position[0] + size[0], position[1] + size[1]
            draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=color)

        big_prime_imgs, activity_big_prime = big_prime()
        for rune, activity in zip(big_prime_imgs, activity_big_prime):
            new_size = (100, 100)
            smaller_image = rune.resize(new_size, Image.Resampling.LANCZOS)
            if activity:
                tinted_image = smaller_image
                canvas.paste(tinted_image, (x, 200), mask=smaller_image)


            else:
 # Opaque background

                tinted_image = ImageOps.colorize(smaller_image.convert("L"), black=(0, 0, 0), white=(50, 50, 100))
                r, g, b, a = smaller_image.split()  # Split the original image into its RGB and alpha channels
                canvas.paste(tinted_image, (x, 200), mask=a)  # Use the alpha channel as the mask
            x += 100

        draw.line([125, 325, 550, 325], fill=(200, 172, 214, 255), width=1)
        draw.text((125, 200), '.', font=font, fill=(200, 172, 214, 255), font_size=20)
        draw.text((125, 330), '.', font=font, fill=(200, 172, 214, 255), font_size=20)
        draw.text((125, 420), '.', font=font, fill=(200, 172, 214, 255), font_size=20)
        draw.text((125, 510), '.', font=font, fill=(200, 172, 214, 255), font_size=20)

        x = 200
        y = 350
        count = 1

        little_prime_imgs, activity_little_prime = little_prime()
        for rune, activity in zip(little_prime_imgs, activity_little_prime):


            new_size = (60, 60)
            smaller_image = rune.resize(new_size, Image.Resampling.LANCZOS)

            if activity:
                tinted_image = smaller_image

                a = smaller_image

            else:

                tinted_image = ImageOps.colorize(smaller_image.convert("L"), black=(0, 0, 0), white=(50, 50, 100))
                r, g, b, a = smaller_image.split()  # Split the original image into its RGB and alpha channels


            a = a.resize(tinted_image.size, Image.Resampling.LANCZOS)

            canvas.paste(tinted_image, (x, y), mask=a)  # Use the alpha channel as the mask
            # Вставка изображения на холст

            # Сдвиг координат по x для следующего изображения
            x += 90
            count += 1

            # Когда вставлено 3 изображения в строку, переходим на новую строку
            if count % 3 == 1:
                x = 200
                y += 90

            # Прекращаем после заполнения 3 строк
            if count == 10:
                break

        mirrored_rectangle_bounds = [
            canvas_width - rectangle_bounds[2],
            rectangle_bounds[1],
            canvas_width - rectangle_bounds[0],
            rectangle_bounds[3],
        ]

        draw.rounded_rectangle(mirrored_rectangle_bounds, radius=30, fill=(46, 35, 108, 255))

        text = en_to_ru[secondary]
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1] + 25

        rect_x1, rect_y1, rect_x2, rect_y2 = mirrored_rectangle_bounds
        rect_width = rect_x2 - rect_x1
        rect_height = rect_y2 - rect_y1

        # Center text position
        text_x = rect_x1 + (rect_width - text_width) / 2
        text_y = rect_y1 + (rect_height - text_height) / 2
        text = en_to_ru[secondary]
        # Draw the text
        draw.text((text_x, text_y), text, font=font, fill=text_color, align='center')
        s_img = fetch_image(secondary_img)
        canvas.paste(s_img, (1100, 50), mask=s_img)

        x = 725
        y = 200

        big_secondary_imgs, activity_big_secondary = big_secondary()
        for rune, activity in zip(big_secondary_imgs, activity_big_secondary):


            draw.text((650, y - 25), '.', font=font, fill=(200, 172, 214, 255), font_size=20)
            new_size = (50, 50)
            smaller_image = rune.resize(new_size, Image.Resampling.LANCZOS)

            # Вставка изображения на холст
            if activity:
                tinted_image = smaller_image
                a = smaller_image


            else:


                tinted_image = ImageOps.colorize(smaller_image.convert("L"), black=(0, 0, 0), white=(50, 50, 100))
                r, g, b, a = smaller_image.split()  # Split the original image into its RGB and alpha channels
            a = a.resize(tinted_image.size, Image.Resampling.LANCZOS)
            canvas.paste(tinted_image, (x, y), mask=a)  # Use the alpha channel as the mask

            # Сдвиг координат по x для следующего изображения
            x += 100
            count += 1

            # Когда вставлено 3 изображения в строку, переходим на новую строку
            if count % 3 == 1:
                x = 725
                y += 70

            # Прекращаем после заполнения 3 строк
            if count == 10:
                break

        draw.line([650, 435, 1075, 435], fill=(200, 172, 214, 255), width=1)

        x = 725
        y = 460
        little_secondary_imgs, activity_little_secondary = little_secondary()

        for rune, activity in zip(little_secondary_imgs, activity_little_secondary):

            y_r = y + 5
            x_r = x + 5
            size = (50, 50)  # Size of the background circle
            radius = 100  # Radius of the rounded corners
            background_color = (46, 35, 108, 255)  # Background color with transparency
            draw.text((650, y - 25), '.', font=font, fill=(200, 172, 214, 255), font_size=20)
            # Draw the rounded background
            draw_rounded_background(draw, (x, y), size, radius, background_color)


            new_size = (40, 40)
            smaller_image = rune.resize(new_size, Image.Resampling.LANCZOS)

            # Draw a rounded background (optional, can be fully transparent)
            if activity:
                draw_rounded_background(draw, (x, y), size, radius, (46, 35, 108, 255))

            else:

                draw_rounded_background(draw, (x, y), size, radius, (46, 35, 108, 255))
                smaller_image.putalpha(10)
                draw_rounded_background(draw, (x, y), size, radius, (46, 35, 108, 255))

            canvas.paste(smaller_image, (x_r, y_r), mask=smaller_image)

            x += 100
            x_r += 100
            count += 1

            # Когда вставлено 3 изображения в строку, переходим на новую строку
            if count % 3 == 1:
                x = 725
                y += 70
                y_r += 70

            # Прекращаем после заполнения 3 строк
            if count == 10:
                break

        save_to_memory_cache(champion, canvas)
        image_id = load_from_memory_cache(champion, 'image_id')

        def image_to_base64(image: Image):
            # Convert the image to a byte stream
            byte_io = io.BytesIO()
            image.save(byte_io, format='PNG')
            byte_io.seek(0)

            # Convert the byte stream to a base64 string
            encoded_image = base64.b64encode(byte_io.read()).decode('utf-8')
            return encoded_image

        def image_to_json(image: Image):
            encoded_image = image_to_base64(image)
            # Create a JSON-compatible dictionary
            json_data = {
                'image': encoded_image
            }
            return json.dumps(json_data)
        print("image generation was successful for " + champion)
        json_data = image_to_json(canvas)
        return json_data
