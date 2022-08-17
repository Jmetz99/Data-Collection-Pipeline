import os
import json
import urllib.request
from selenium import webdriver
import time
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GorillaMindScraper:
    '''
    This class is used to represent the Gorilla Mind website to be scraped.

    Attributes:
    url (str): The url link to the website to be scraped.
    '''


    def __init__(self, url):
        '''
        Constructs the necessary attributes for the scraper object and sets the webdriver to Selenium.
        
        Parameters:
        url (str): The url link to the website to be scraped.
        '''
        self.url = url
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
       
    def __open_page(self):
        '''
        This function is used to open the webpage given.
        '''
        self.driver.get(self.url)

    def get_links(self):
        '''
        This function is used to obtain the links to product pages.
        
        Returns:
            list: The list of links to product pages.
        '''
        self.driver.get(self.url)
        prod_container = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]')
        prod_list = prod_container.find_elements(by=By.XPATH, value = './div')
        link_list = []
        for product in prod_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        return link_list

    def click_product(self):
        '''
        This function is used to click on a product.
        '''
        product = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/a')
        product.click()

    def scroll_to_next_page_button(self):
        '''
        This function is used to scroll down to the next page button.
        '''
        time.sleep(3)
        next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
        self.driver.execute_script("arguments[0].scrollIntoView();", next_page)

    def close_offer(self):
        '''
        This function is used to close the discount offer pop-up window.
        '''
        delay = 10
        close_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SMSBump-Modal"]/div/div/button')))
        close_button.click()

    def go_to_next_page(self):
        '''
        This function is used to navigate to the next page of products.
        '''
        next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
        next_page.click()
    
    def get_product_data(self, link):
        '''
        This function is used to create a dictionary containing all product data.

        Parameters:
        link (str): The link to the product page.

        Returns:
            dict: The dictionary containing all product data.
        '''
        product_dict = {'Name': [], 'ID': '', 'UUID': [], 'Price': [], 'Description': [], 'Flavours': [], 'Rating': [], 'Image Link': ""}
        self.driver.get(link)
        product_dict['ID'] = self.product_id(link)
        product_dict['UUID'] = uuid.uuid4()
        product_dict['Image Link'] = self.extract_image_link(link)
        try:
            product_dict['Name'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/h1').text
        except:
            print('Data not found.')
        
        try:
            product_dict['Price'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/p').text   
        except:
            print('Data not found.')

        try:
            product_dict['Description'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[2]/div/div/div[1]/div/div[1]/div[1]/span[1]').text
        except:
            print('Data not found.')

        try:
            flavours = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/section/div/div[2]/section[1]/section/div/div/div[2]/div[5]/div[2]/form/div[2]/div[1]').text
            flavour_list = list(flavours.splitlines())
            product_dict['Flavours'] = flavour_list.remove('Flavor')
        except:
            print('Data not found.')
        
        try:
            product_dict['Rating'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-68eb7e26-87f6-4711-8408-2327df293f70"]/section/div/div/div/div/span/div[1]/div/div[1]/span').text
        except:
            print('Data not found.')
        
        return product_dict

    def product_id(self, link):
        '''
        This function is used to generate a product ID and append it to that product's dictionary.
        
        Parameters:
            link(str): The link to the product page.
        '''
        id = link.replace('https://gorillamind.com/collections/all/products/', '')
        return id
        

    def extract_image_link(self, link):
        '''
        This function is used to extract the link to a product's image and append it to that product's dictionary.
        
        Parameters:
            link(str): The link to the product page.
        '''
        self.driver.get(link)
        image_HTML = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/section/div/div[2]/section[1]/section/div/div/div[1]/div/div[1]/div/div/div[1]/div/img')
        src = image_HTML.get_attribute('src')
        image_link = str(src)
        return image_link
    
    def save_data(self, data):
        '''
        This function is used to save a product dictionary.

        This function creates a new directory named after the product's ID and then saves 
        the product's dictionary as a .json file within this directory.
        '''
        directory = data["ID"]
        parent_directory = "/Users/jacobmetz/Documents/web_scraper/raw_data/"
        path = os.path.join(parent_directory, directory)
        os.mkdir(path)
        with open('{name}/data.json'.format(name = data["ID"]), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def download_image(self, link):
        '''
        This function is used to save a product image
        
        This function retrives a product's image through the link in its dictionary and saves
        the image within that product's directory.
        '''
        data = self.get_product_data(self, link)
        image_link = data["Image Link"]
        id = data["ID"]
        parent_directory = "/Users/jacobmetz/Documents/web_scraper/raw_data/"
        path = os.path.join(parent_directory, id)
        urllib.request.urlretrieve(image_link, "%s/id.jpeg" %path)

if __name__ == '__main__':
    scraper = GorillaMindScraper('https://gorillamind.com/collections/all?page=1')
    links = scraper.get_links()
    print(links)