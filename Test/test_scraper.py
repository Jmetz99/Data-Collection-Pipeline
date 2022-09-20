import sys
import unittest
import json
import os
sys.path.insert(1, '/Users/jacobmetz/Documents/web_scraper/utils')
from scraper import Scraper

class ScraperTestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.test_scraper = Scraper()
        self.link_list = self.test_scraper.get_links()
    
    def test_get_links(self):
        self.assertEqual(len(self.link_list), 48)

    def test_get_product_data(self):
        product_dict = self.test_scraper.get_product_data(self.link_list[1])

        self.assertIsInstance(product_dict['Description'], str)
        self.assertEqual(product_dict['ID'], 'gorilla-mode-nitric')
        dollar = '$'
        price = product_dict['Price']
        is_dol_present = price.find(dollar)
        self.assertEqual(is_dol_present, 0)
        self.assertIsInstance(product_dict['Flavours'], list)
        self.assertIsInstance(product_dict['Rating'], float)
        self.assertIsInstance(product_dict['Image Link'], str)

    def mk_test_datafolder(self):
        id = self.test_scraper._product_id(self.link_list[1])
        path = f'{os.getcwd()}/raw_data_test/{id}'
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)
        return path
    
    def delete_test_datafolder(self):
            path = self.mk_test_datafolder()
            os.rmdir(path)

    def test_save_data(self):
        path = self.mk_test_datafolder()
        data = self.test_scraper.get_product_data(self.link_list[1])
        self.test_scraper.save_data(data, path)
        id = self.test_scraper._product_id(self.link_list[1])
        with open(f"/Users/jacobmetz/Documents/web_scraper/test/comparison_data/{id}/data.json", "r") as f1:
            file1 = json.loads(f1.read())
        with open(f"{path}/data.json", "r") as f2:
            file2 = json.loads(f2.read())
        self.assertEqual(file1, file2)
        self.delete_test_datafolder()

if __name__ == '__main__':
    unittest.main()
