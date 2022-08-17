import unittest
from context import project

scraper = project.GorillaMindScraper('https://gorillamind.com/collections/all?page=1')

class ScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_get_links(self):
        link_list = scraper.get_links()
        self.assertEqual(len(link_list), 48)

if __name__ == '__main__':
    unittest.main()
