import requests
import os
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request
import os
import logging
from databases import Database
import environ

env = environ.Env()

logger = logging.Logger(__name__)

HOST = env("RDS_HOSTNAME", default="localhost")
NAME = env("RDS_DB_NAME", default="image_db")
PORT = env("RDS_PORT", default="5432")
USER = env("RDS_USERNAME", default="postgres")
PASSWORD = env("RDS_PASSWORD", default="postgres")

database = Database(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}")


async def save_to_db(file_path: str):
    query = """INSERT INTO public.google_images(file_path) VALUES (:file_path);"""

    try:
        await database.connect()
        logger.info("Connected to Database")
        await database.execute(query=query, values={"file_path": file_path})
        await database.disconnect()
        logger.info("Disconnecting from Database")
    except Exception as ex:
        logger.exception(ex)


async def download_image(url: str, filename: str):
    try:
        urllib.request.urlretrieve(url, filename)
        await save_to_db(filename)
    except Exception as ex:
        logger.exception(ex)


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
    tasks = []
    for i, url in enumerate(image_urls):
        filename = f"downloaded/{query}/{i+1}.jpg"
        tasks.append(asyncio.create_task(download_image(url, filename)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    query = input("Enter search query: ")
    num_images = int(input("Enter number of images to download: "))

    asyncio.run(main(query, num_images))
