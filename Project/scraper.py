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
import boto3
import pandas as pd
from sqlalchemy import create_engine

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
    
    def _close_page(self):
        '''
        This function is used to quit the browser.
        '''
        self.driver.quit()

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

    def __click_product(self):
        '''
        This function is used to click on a product.
        '''
        product = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/a')
        product.click()

    def __scroll_to_next_page_button(self):
        '''
        This function is used to scroll down to the next page button.
        '''
        time.sleep(3)
        next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
        self.driver.execute_script("arguments[0].scrollIntoView();", next_page)

    def __close_offer(self):
        '''
        This function is used to close the discount offer pop-up window.
        '''
        delay = 10
        close_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SMSBump-Modal"]/div/div/button')))
        close_button.click()

    def __go_to_next_page(self):
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
        product_dict = {'Name': '', 'ID': '', 'UUID': '', 'Price': 0, 'Description': '', 'Number of Flavours': [], 'Rating': 0, 'Image Link': ""}
        self.driver.get(link)
        product_dict['ID'] = self._product_id(link)
        UUID = str(uuid.uuid4())
        UUID_1 = UUID.strip("UUID('")
        UUID_2 = UUID_1.strip(")'")
        product_dict['UUID'] = UUID_2
        product_dict['Image Link'] = self._extract_image_link()
        try:
            product_dict['Name'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/h1').text
        except:
            print('Name not found.')
        
        try:
            product_dict['Price'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/p/span[2]/span/span').text
        except:
            print(f'{product_dict["ID"]} price not found.')

        try:
            descrip_txt = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[2]/div/div/div[1]/div/div[1]/div[1]/span[1]').text
            description = descrip_txt.replace('\n', " ")
            product_dict['Description'] = description
        except:
            print(f'{product_dict["ID"]} description not found.')

        try:
            flavours = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/section/div/div[2]/section[1]/section/div/div/div[2]/div[5]/div[2]/form/div[2]/div[1]').text
            flavour_list = flavours.splitlines()
            flavour_list.remove('Flavor')
            product_dict['Number of Flavours'] = len(flavour_list)
        except:
            print(f'{product_dict["ID"]} flavours not found.')
        
        try:
            rating = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-68eb7e26-87f6-4711-8408-2327df293f70"]/section/div/div/div/div/span/div[1]/div/div[1]/span').text
            rating = float(rating)
            product_dict['Rating'] = rating
        except:
            print(f'{product_dict["ID"]} rating not found.')
        
        return product_dict

    def _product_id(self, link):
        '''
        This function is used to generate a product ID from its web address.
        
        Parameters:
            link(str): The link to the product page.
        '''
        id = link.replace('https://gorillamind.com/collections/all/products/', '')
        if id[0:5] == 'https':
            id = link.replace('https://gorillamind.com/products/', '')    
        return id
        

    def _extract_image_link(self):
        '''
        This function is used to extract the link to a product's image from its web page.
        
        Parameters:
            link(str): The link to the product page.
        '''
        image_HTML = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/section/div/div[2]/section[1]/section/div/div/div[1]/div/div[1]/div/div/div[1]/div/img')
        src = image_HTML.get_attribute('src')
        image_link = str(src)
        return image_link

    def get_path_to_data(self, link):
        '''
        This function is used to create the path to the local folder for a given product from its product page link.
        
        Parameters:
            link(str): The link to the product page.
        '''
        id = self._product_id(link)
        cwd = os.getcwd()
        path = f'{cwd}/raw_data/{id}' 
        return path
    
    def make_directory(self, path):
        '''
        This function is used to create a local folder for a given product in a specificed location.
        
        Parameters:
            path(str): The path to the local folder.
        '''
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

    def save_data(self, data, directory):
        '''
        This function is used to save the data of a product in a specified directory.
        '''
        os.chdir(directory)
        with open('data.json'.format(name = data["ID"]), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def download_image(self, image_link, id, path):
        '''
        This function is used to save a product image in a specified directory.
        
        This function retrives a product's image through the link given and saves
        the image within the specified directory.
        '''
        os.chdir(path)
        urllib.request.urlretrieve(image_link, f"{id}.jpeg")
    
    def upload_to_cloud(self, path):
        '''
        This function is used to upload a given product's json file to an amazon S3 bucket.
        Parameters:
            link(str): The link to the product page.
        '''
        s3_client = boto3.client('s3')
        id = path.replace('/Users/jacobmetz/Documents/web_scraper/project/raw_data/', '')
        response = s3_client.upload_file(f'{path}/data.json', 'aicore-scraper-data', f'{id}.json')
        reponse = s3_client.upload_file(f'{path}/{id}.jpeg', 'aicore-scraper-data', f'{id}.jpeg')
    
    def get_all_data(self):
        links = self.get_links()
        data_dicts = []

        for link in links:
            data = scraper.get_product_data(link)
            data_dicts.append(data)
            path = scraper.get_path_to_data(link)
            directory = scraper.make_directory(path)
            scraper.save_data(data, path)
            scraper.download_image(data['Image Link'], data['ID'], path)
            scraper._close_page()
        return data_dicts
    



if __name__ == '__main__':
    scraper = GorillaMindScraper('https://gorillamind.com/collections/all?page=1')
    all_data = scraper.get_all_data()
    df = pd.DataFrame(all_data)
    print(df)

    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = 'aicore-scraper-data.cjzhidft7nnj.eu-west-2.rds.amazonaws.com'
    USER = 'postgres'
    os.chdir('/Users/jacobmetz/Desktop')
    with open('password.txt', 'rb') as fp:
        PASSWORD = fp.read()
    DATABASE = 'GorillaMindProductData'
    PORT = 5432
    engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    engine.connect()
    os.chdir('/Users/jacobmetz/Desktop')
    with open('password.txt', 'rb') as fp:
        PASSWORD = fp.read()
        print(v)
    df.to_sql('aicore-scraper-data', engine, if_exists='replace')
