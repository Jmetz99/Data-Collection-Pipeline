import unittest
from context import project
import imghdr
import os

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = project.GorillaMindScraper('https://gorillamind.com/collections/all?page=1')
    
    # def test_get_links(self):
    #     link_list = self.scraper.get_links()
    #     self.assertEqual(len(link_list), 48)

    # def test_get_product_data(self):
    #     product_dict = self.scraper.get_product_data('https://gorillamind.com/products/gorilla-mode-nitric')
    #     self.assertIsInstance(product_dict['Description'], str)
    #     self.assertEqual(product_dict['ID'], 'gorilla-mode-nitric')
    #     dollar = '$'
    #     price = product_dict['Price']
    #     is_dol_present = price.find(dollar)
    #     self.assertEqual(is_dol_present, 0)
    #     self.assertIsInstance(product_dict['Flavours'], list)
    #     self.assertIsInstance(product_dict['Rating'], int)
    #     self.assertIsInstance(product_dict['Image Link'], str)

    def test_save_data(self):
        
        self.scraper.download_image('https://gorillamind.com/products/gorilla-mode-nitric')
        
        


if __name__ == '__main__':
    unittest.main()
