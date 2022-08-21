import unittest
from context import project
import json
import os

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.test_scraper = project.GorillaMindScraper('https://gorillamind.com/collections/all?page=1')
        self.link_list = self.test_scraper.get_links()

    def test_get_links(self):
        link_list = self.test_scraper.get_links()
        self.assertEqual(len(link_list), 48)

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

    def mk_test_database(self):
        id = self.test_scraper._product_id(self.link_list[1])
        path = f'{os.getcwd()}/raw_data_test/{id}'
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)
        return path
    
    def delete_test_database(self):
            path = self.mk_test_database()
            os.rmdir(path)

    def test_save_data(self):
        path = self.mk_test_database()
        data = self.test_scraper.get_product_data(self.link_list[1])
        self.test_scraper.save_data(data, path)
        id = self.test_scraper._product_id(self.link_list[1])
        with open(f"/Users/jacobmetz/Documents/web_scraper/test/comparison_data/{id}/data.json", "r") as f1:
            file1 = json.loads(f1.read())
        with open(f"{path}/data.json", "r") as f2:
            file2 = json.loads(f2.read())
        self.assertEqual(file1, file2)
        self.delete_test_database()

if __name__ == '__main__':
    unittest.main()
