import asyncio
import logging
import unittest

from dl_image import download_image, main, resize_image, save_to_db

logger = logging.getLogger(__name__)


class DlImageTest(unittest.IsolatedAsyncioTestCase):
    async def test_db1(self):
        result = await save_to_db("/salam")
        self.assertTrue(result)

    async def test_db2(self):
        result = await save_to_db(123)
        self.assertFalse(result)

    async def test_download_image1(self):
        url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVeEiZtBzWrF_QzbjLyLBKiIxK4QdscZ5_RlOUutunmi8XrtZamNwuIssvIQ&s"
        filename = "downloaded/cute+kittens/1.jpg"

        result = await download_image(url, filename)
        self.assertTrue(result)

    async def test_download_image2(self):
        url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVeEiZtBzWrF_zbjLyLBKiIxK4QdscZ5_lOUutunmi8XrtZamNwuIssvIQ&s"
        filename = "downloaded/cute+kittens/some_false_image.jpg"

        result = await download_image(url, filename)
        self.assertFalse(result)

    async def test_resize_image1(self):
        result = await resize_image("downloaded/cute+kittens/1.jpg")
        self.assertTrue(result)

    async def test_resize_image2(self):
        result = await resize_image("downloaded/wrong_folder/some_false_image.jpg")
        self.assertFalse(result)

    # def test(self):
    #     asyncio.run(main("something cute", 3))


if __name__ == "__main__":
    logger.setLevel("DEBUG")
    unittest.main()
