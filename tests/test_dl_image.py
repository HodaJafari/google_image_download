import unittest
import logging
from dl_image import test

logger = logging.getLogger(__name__)

class DlImageTest(unittest.TestCase):
    def test(self):
        self.assertTrue(test())

if __name__ == "__main__":
    logger.setLevel("DEBUG")
    unittest.main()