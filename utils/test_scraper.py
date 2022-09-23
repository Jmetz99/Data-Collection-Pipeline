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
     
    @patch('scraper.Scraper.close_offer')
    @patch('scraper.Scraper.click_object')
    def test_get_links(self, 
        mock_click_object: Mock, 
        mock_close_offer: Mock
        ):
        link_list = self.scraper.get_links()
        mock_close_offer.assert_called_once()
        mock_click_object.assert_called_once()
        self.assertGreaterEqual(len(link_list), 48)


    def test_get_product_data(self):
        product_dict = self.scraper.get_product_data('https://gorillamind.com/products/gorilla-mode')

        self.assertIsInstance(product_dict['Description'], str)
        self.assertEqual(product_dict['ID'], 'gorilla-mode')
        dollar = '$'
        price = product_dict['Price']
        is_dol_present = price.find(dollar)
        self.assertEqual(is_dol_present, 0)
        self.assertIsInstance(product_dict['Flavours'], list)
        self.assertIsInstance(product_dict['Rating'], float)
        self.assertIsInstance(product_dict['Image Link'], str)

    # def mk_test_datafolder(self):
    #     id = self.test_scraper._product_id(self.link_list[1])
    #     path = f'{os.getcwd()}/raw_data_test/{id}'
    #     if os.path.exists(path):
    #         pass
    #     else:
    #         os.makedirs(path)
    #     return path
    
    # def delete_test_datafolder(self):
    #         path = self.mk_test_datafolder()
    #         os.rmdir(path)

    def test_save_data(self):
        
        data = self.scraper.get_product_data(self.link_list[1])
        self.test_scraper.save_data(data, path)
        id = self.test_scraper._product_id(self.link_list[1])
        with open(f"/Users/jacobmetz/Documents/web_scraper/test/comparison_data/{id}/data.json", "r") as f1:
            file1 = json.loads(f1.read())
        with open(f"{path}/data.json", "r") as f2:
            file2 = json.loads(f2.read())
        self.assertEqual(file1, file2)
        self.delete_test_datafolder()

    def tearDown(self):
        self.scraper.driver.quit()
        del self.scraper

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
