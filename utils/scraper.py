import os
import json
import chromedriver_autoinstaller as chromedriver
from selenium import webdriver
import urllib.request
import time
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import boto3
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'gorilla.cjzhidft7nnj.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = os.environ.get('Password')
DATABASE = 'postgres'
PORT = 5432
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
engine.connect()
chromedriver.install()


class Scraper:
    '''
    This class is used to represent the Gorilla Mind website to be scraped.

    Attributes:
    ----------
    url: str
        The url link to the website to be scraped.
    '''

    def __init__(self, url: str = 'https://gorillamind.com/collections/all?page=1'):
        '''
        Constructs the necessary attributes for the scraper object and sets the webdriver to Selenium.
        
        Parameters:
        ----------
        url: str 
            The url of the website to be scraped.
        '''
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        self.driver.maximize_window()

    def click_object(self, xpath: str):
        '''
        This function is used to click on an object.
        
        Parameters:
        ----------
        xpath: str
            The Xpath of the object to be clicked
        '''
        product = self.driver.find_element(by=By.XPATH, value = xpath)
        product.click()

    def close_offer(self, xpath: str = '//button[@class="needsclick klaviyo-close-form kl-private-reset-css-Xuajs1"]'):
        '''
        This function is used to close the discount offer pop-up window.

        Parameters:
        ----------
        xpath: str
            The Xpath of the pop-up window.
        '''

        close_offer_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        close_offer_button.click()

    def get_links(self, xpath: str = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]'):
        '''
        This function is used to obtain the links to product pages.
        
        Parameters:
        ----------
        xpath: str
            The Xpath of the product container.
        
        Returns:
        -------
        link_list: list
            The list of links to product pages.
        '''
        prod_container1 = self.driver.find_element(by=By.XPATH, value = xpath)
        prod_list1 = prod_container1.find_elements(by=By.XPATH, value = './div')
        link_list = []
        for product in prod_list1:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)

        self.close_offer()
        self.click_object('//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')

        prod_container2 = self.driver.find_element(by=By.XPATH, value = xpath)
        prod_list2 = prod_container2.find_elements(by=By.XPATH, value = './div')
        for product in prod_list2:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        return link_list
    
    def extract_image_link(self, xpath: str = '//*[@class="image__container"]'):
        '''
        This function is used to extract the link to a product's image from its web page.
        
        Parameters:
        ----------
        xpath: str
            The xpath of the product's image tag.
        '''
        try:
            container = self.driver.find_element(by=By.XPATH, value=xpath)
            img_tag = container.find_element(by=By.TAG_NAME, value='img')
            src = img_tag.get_attribute('src')
            image_link = str(src)
            return image_link
        except:
            pass


    def _product_id(self, link):
        '''
        This function is used to generate a product ID from its web address.
        
        Parameters:
        ----------
        link: str
            The link to the product page.

        Returns:
        --------
        id: str 
            The user friendly id of product.
        '''
        id = link.replace('https://gorillamind.com/collections/all/products/', '')
        if id[0:5] == 'https':
            id = link.replace('https://gorillamind.com/products/', '')    
        return id

    def get_product_data(self, link):
        '''
        This function is used to create a dictionary containing all product data.

        Parameters:
        ----------
        link: str
            The link to the product page

        Returns:
        --------
        product_dict: dict 
            The dictionary containing all of a product's data.
        '''
        product_dict = {'Name': '', 'ID': '', 'UUID': '', 'Price': 0, 'Description': '', 'Number of Flavours': [], 'Rating': 0, 'Image Link': ""}
        self.driver.get(link)
        product_dict['Image Link'] = self.extract_image_link()
        product_dict['ID'] = self._product_id(link)
        UUID = str(uuid.uuid4())
        UUID_1 = UUID.strip("UUID('")
        UUID_2 = UUID_1.strip(")'")
        product_dict['UUID'] = UUID_2
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
            descrip_txt = self.driver.find_element(by=By.XPATH, value='//*[@class="image-with-text__text text-align-left content"]').text
            descrip_txt.replace('\n', " ")
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

    def get_path_to_data(self, link):
        '''
        This function is used to create the path to the local folder for a given product from its product page link.
        
        Parameters:
        ----------
        link: str
            The link to the product page.
       
        Returns:
        --------
        path: str
            The path to the local folder.
        '''
        id = self._product_id(link)
        cwd = os.path.dirname(os.path.realpath(__file__))
        path = f'{cwd}/raw_data/{id}' 
        return path

    def make_directory(self, path):
        '''
        This function is used to create a local folder for a given product in a specificed location.
        
        Parameters:
        ----------
        path: str
            The path to the local folder.
        '''
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

    def save_data(self, data, path):
        '''
        This function is used to save the data of a product in a specified directory.

        Parameters:
        ----------
        data: dict
            The dictionary of product data
        path: str
            The path to the local folder.
        '''
        os.chdir(path)
        with open('data.json'.format(name = data["ID"]), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def download_image(self, image_link, id, path):
        '''
        This function is used to save a product image in a specified directory.
        
        Parameters:
        ----------
        image_link: str
            The link to the product image.
        id: str
            The id of the product.
        path: str
            The path to the local folder.
        '''
        os.chdir(path)
        try:
            urllib.request.urlretrieve(image_link, f"{id}.png")
        except:
            print(f'{id} image not found')
    
    def _return_home(self):
        '''
        This function is used to return to the root project folder.
        '''
        p = os.path.abspath(os.path.dirname(__file__))
        os.chdir(p)
    
    def upload_to_cloud(self, path):
        '''
        This function is used to upload a given product's json file to an amazon S3 bucket.

        Parameters:
        ----------
        path: str
            The path to the local folder.
        '''
        s3_client = boto3.client('s3')
        id = path.replace('/Users/jacobmetz/Documents/web_scraper/utils/raw_data/', '')
        
        s3_client.upload_file(f'{path}/data.json', 'aicore-scraper-data', f'{id}.json')
        try:
            s3_client.upload_file(f'{path}/{id}.jpeg', 'aicore-scraper-data', f'{id}.jpeg')
        except:
            pass
    
    def _get_unscraped_links(self):
        '''
        This function prevents rescraping by comparing scraped ids with the ids of already scraped products in the SQL database.
        
        Returns:
        --------
        links_to_scrape: list
            The list of unscraped links.
        '''
        links = self.get_links()
        ids = set()
        for link in links:
            uids = []
            id = self._product_id(link)
            uids.append(id)
            ids.update(uids)
        
        db_ids = pd.read_sql_query('''SELECT "ID" FROM "GorillaMindProductData"''', engine)
        old_ids = set(db_ids["ID"])
        sym_diff = list(ids.symmetric_difference(old_ids))
        
        links_to_scrape = []
        for id in sym_diff:
            link = f"https://gorillamind.com/collections/all/products/{id}"
            links_to_scrape.append(link)
        if len(links_to_scrape) == 0:
            print('Up to date!')
        
        return links_to_scrape

    def scrape_all_data(self):
        '''
        This function is used scrape all new product data from the gorilla mind website and return a dataframe of the scraped data.
        '''
        links = self._get_unscraped_links()
        data_dicts = []

        for link in links:
            data = self.get_product_data(link)
            data_dicts.append(data)
            path = self.get_path_to_data(link)
            self.make_directory(path)
            self.save_data(data, path)
            self.download_image(data['Image Link'], data['ID'], path)
            self.upload_to_cloud(path)
            self._return_home()

        df = pd.DataFrame(data_dicts)
        return df