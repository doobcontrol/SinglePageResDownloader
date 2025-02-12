import unittest
from pageScraper import pgScraper

class TestpgScraper_findIndex_between(unittest.TestCase):

    def  setUp(self):
        self.pS = pgScraper()

    def test_pgScraper_findIndex_between(self):
            fb = self.pS.findIndex_between
            ae = self.assertEqual
            ae(fb('cccazzzzzbccc','a','b'), (4, 9))
            ae(fb('cccazzzzzbccc','a','b', 2), (4, 9))
            ae(fb('cccazzzzzbccc','a','b', 4), None)

    def test_pgScraper_find_between(self):
            fb = self.pS.find_between
            ae = self.assertEqual
            ae(fb('cccazzzzzbccc','a','b'), 'zzzzz')
            ae(fb('cccazzzzzbccc','a','b', 2), 'zzzzz')
            ae(fb('cccazzzzzbccc','a','b', 4), None)

    def test_pgScraper_find_allBetween(self):
            fb = self.pS.find_allBetween
            ae = self.assertEqual
            ae(fb('cccazbzzazzbccc','a','b'), ['z','zz'])
            ae(fb('cccazbzzazzbccc','a','b', 4), ['zz'])
            ae(fb('cccazzzazzbccc','a','b'), ['zz'])
            
    def test_pgScraper_washPathStr(self):
            ws = self.pS.washPathStr
            ae = self.assertEqual
            testStr = 'cccazzzzzbccc'
            for i in self.pS.illegalChrs:
                testStr += i
            ae(ws(testStr),'cccazzzzzbccc')

if __name__ == '__main__':
   unittest.main()
