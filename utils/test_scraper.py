import json
import os
from scraper import Scraper
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    def test_get_links(self):
        self.scraper.driver.get('https://gorillamind.com/collections/all?page=1')
        link_list = self.scraper.get_links()
        self.assertGreaterEqual(len(link_list), 48)

    def test_get_product_data(self):
        product_dict = self.scraper.get_product_data('https://gorillamind.com/products/gorilla-mode')
        self.assertIsInstance(product_dict['Description'], str)
        self.assertEqual(product_dict['ID'], 'gorilla-mode')
        dollar = '$'
        price = product_dict['Price']
        is_dol_present = price.find(dollar)
        self.assertEqual(is_dol_present, 0)
        self.assertIsInstance(product_dict['Number of Flavours'], int)
        self.assertIsInstance(product_dict['Rating'], float)
        self.assertIsInstance(product_dict['Image Link'], str)
    
    def test_make_directory(self):
        directory_path = '/Users/jacobmetz/Documents/web_scraper/utils/gorilla'
        self.scraper.make_directory(directory_path)
        self.assertTrue(os.path.exists(directory_path))
        os.rmdir('/Users/jacobmetz/Documents/web_scraper/utils/gorilla')
    
    # @patch(scraper.scraper)
    # def test_save_data(self):
    #     data = self.scraper.get_product_data()
    #     self.scraper.save_data(data, path)
    #     id = self.test_scraper._product_id()
    #     with open(f"/Users/jacobmetz/Documents/web_scraper/test/comparison_data/{id}/data.json", "r") as f1:
    #         file1 = json.loads(f1.read())
    #     with open(f"{path}/data.json", "r") as f2:
    #         file2 = json.loads(f2.read())
    #     self.assertEqual(file1, file2)

    def tearDown(self):
        self.scraper.driver.quit()
        del self.scraper

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
