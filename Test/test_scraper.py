import unittest
from Project import scraper

class ScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_get_links(self):
        link_list = Project.GorillaMindScraper.get_links()
        self.assertEqual(len(link_list), 48)

if __name__ == '__main__':
    unittest.main()
