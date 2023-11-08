import asyncio
import logging
import os
import urllib.request
from urllib.parse import quote

import asyncpg
import environ
import requests
from bs4 import BeautifulSoup
from PIL import Image

env = environ.Env()

logger = logging.getLogger(__name__)

USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5432"
DB_NAME = "image_db"


async def save_to_db(file_path: str):
    query = """INSERT INTO public.google_images(file_path) VALUES ($1);"""

    try:
        conn = await asyncpg.connect(
            user=USER, password=PASSWORD, database=DB_NAME, host=HOST, port=PORT
        )
        logger.info("Connected to Database")

        await conn.execute(query, file_path)
        await conn.close()
        logger.info("Disconnecting from Database")

    except Exception as ex:
        logger.exception(ex)
        return False
    return True


async def download_image(url: str, filename: str):
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception as ex:
        logger.exception(ex)
        return False
    return True


async def resize_image(image_path, width=100, height=100):
    # Resize the image
    try:
        image = Image.open(image_path)
        resized_image = image.thumbnail((width, height))
        if resized_image:
            resized_image.save(image_path)
            logger.info(f"Image resized successfully.")
    except Exception as ex:
        logger.exception(ex)
        return False
    return True


async def save_image(url: str, filename: str):
    await download_image(url, filename)
    await resize_image(filename)
    await save_to_db(filename)


async def get_image_urls(query: str, num_images: int):
    query = quote(query)
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the image elements in the HTML
    images = soup.find_all("img")

    image_urls = []
    # Download the first n images
    count = 0
    for image in images:
        if count == num_images:
            break

        image_url = image["src"]
        if len(image_url) >= 4 and image_url[-4:] != ".gif":
            image_urls.append(image_url)
            count += 1

    return image_urls


async def main(query: str, num_images: int):
    query = query.replace(" ", "+")

    # Create a directory to save the images
    if not os.path.exists(f"downloaded/{query}"):
        os.makedirs(f"downloaded/{query}")

    image_urls = await get_image_urls(query, num_images)
    tasks = set()
    for i, url in enumerate(image_urls):
        filename = f"downloaded/{query}/{i+1}.jpg"
        tasks.add(asyncio.create_task(save_image(url, filename)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    query = input("Enter search query: ")
    num_images = int(input("Enter number of images to download: "))

    HOST = input("Enter PostgreSQL Host (default: localhost): ")
    if HOST == "":
        HOST = "localhost"
    PORT = input("Enter PostgreSQL port (default: 5432): ")
    if PORT == "":
        PORT = "5432"
    DB_NAME = input("Enter PostgreSQL image_db (default: image_db): ")
    if DB_NAME == "":
        DB_NAME = "image_db"
    USER = input("Enter PostgreSQL user (default: postgres): ")
    if USER == "":
        USER = "postgres"
    PASSWORD = input("Enter PostgreSQL password (default: postgres): ")
    if PASSWORD == "":
        PASSWORD = "postgres"

    asyncio.run(main(query, num_images))
