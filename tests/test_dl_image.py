import unittest
import logging
from dl_image import main
import asyncio

logger = logging.getLogger(__name__)


class DlImageTest(unittest.TestCase):
    def test(self):
        asyncio.run(main("something cute", 3))


if __name__ == "__main__":
    logger.setLevel("DEBUG")
    unittest.main()
