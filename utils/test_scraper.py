import json
import os
import imghdr
from scraper import Scraper
import sys
import unittest
import shutil

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    def test_close_offer(self):
        self.scraper.driver.get('https://gorillamind.com/collections/all?page=1')
        self.scraper.driver.maximize_window()
        self.scraper.close_offer()
        hidden_pop = self.scraper.driver.find_element_by_xpath('//button[@class="needsclick kl-teaser-Y7HNgj undefined kl-private-reset-css-Xuajs1"]')
        hidden_pop_class = hidden_pop.get_attribute("class")
        self.assertEqual('needsclick kl-teaser-Y7HNgj undefined kl-private-reset-css-Xuajs1', hidden_pop_class)

    def test_get_links(self):
        self.scraper.driver.get('https://gorillamind.com/collections/all?page=1')
        self.scraper.driver.maximize_window()
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

    def test_get_path_to_data(self):
        path = self.scraper.get_path_to_data('https://gorillamind.com/products/gorilla-mode')
        self.assertEqual(path, '/Users/jacobmetz/Documents/web_scraper/utils/raw_data/gorilla-mode')
    
    def test_save_data(self):
        data = {'Name': 'Gorilla', 'ID': 'gorilla-man', 'Rating': '10.0', 'Flavours': '99'}
        path = '/Users/jacobmetz/Documents/web_scraper/utils/raw_data_test'
        self.scraper.make_directory(path)
        self.scraper.save_data(data, path)
        f = open('/Users/jacobmetz/Documents/web_scraper/utils/raw_data_test/data.json')
        saved_data = json.load(f)
        self.assertEqual(saved_data['ID'], data['ID'])
        self.assertEqual(saved_data['Rating'], data['Rating'])
        shutil.rmtree(path)

    def test_download_image(self):
        image_link = "https://cdn.shopify.com/s/files/1/0369/2580/0493/products/Gorilla-Mode-Cherry-Blackout_1200x.png?v=1663603113"
        path = '/Users/jacobmetz/Documents/web_scraper/utils/raw_data_test'
        id = 'gorilla'
        self.scraper.make_directory(path)
        self.scraper.download_image(image_link, id, path)
        self.assertEqual(imghdr.what('/Users/jacobmetz/Documents/web_scraper/utils/raw_data_test/gorilla.jpeg'), 'png')
        shutil.rmtree(path)

    # def test_upload_to_cloud(self):


    def tearDown(self):
        self.scraper.driver.quit()
        del self.scraper

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
