import unittest
from pageScraper import WrongUrlException, ItemsNotFoundError
from pconlinePageScraper import pconlinePgScraper

class TestfengniaoPgScraper(unittest.TestCase):

    def  setUp(self):
        self.pS = pconlinePgScraper()
        import gettext
        # Set up Gettext
        en_i18n = gettext.translation("test", fallback=True)
        # Create the "magic" function
        en_i18n.install()        

    def test_fengniaoPgScraper_downloadPics_wrongUrl(self):
        for url in ["fsafdsaf",
                    "https://github.com/",
                    "https://dp.pconline.com.cn/photo"]:
            with self.subTest(url=url):
                with self.assertRaises(WrongUrlException):
                    self.pS.downloadPics(url)

if __name__ == '__main__':
   unittest.main()
