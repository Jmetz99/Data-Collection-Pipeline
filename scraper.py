from ast import Try
from selenium import webdriver
import time
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GorillaMindScraper:
    if __name__ == "__main__":
        def __init__(self, url):
            self.url = url
            chrome_options = Options()
            self.driver = webdriver.Chrome(options=chrome_options)
            self.product_dict = {'Name': [], 'ID': [], 'UUID': [], 'Price': [], 'Description': [], 'Flavours': [], 'Rating': [], 'Image Link': []}

            
        def open_page(self, url):
            self.driver.get(url)

        def get_links(self):
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
            product = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/a')
            product.click()

        def scroll_to_next_page_button(self):
            time.sleep(3)
            next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
            self.driver.execute_script("arguments[0].scrollIntoView();", next_page)

        def close_offer(self):
            delay = 10
            close_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SMSBump-Modal"]/div/div/button')))
            close_button.click()

        def go_to_next_page(self):
            next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
            next_page.click()
        
        def extract_text(self, link):
                self.driver.get(link)

                try:
                    name = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/h1').text
                    self.product_dict['Name'].append(name)
                except:
                    pass
                
                try:
                    price = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/p').text
                    self.product_dict['Price'].append(price)
                except:
                    pass

                try:
                    description = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[2]/div/div/div[1]/div/div[1]/div[1]/span[1]').text
                    self.product_dict['Description'].append(description)
                except:
                    pass

                try:
                    flavours = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/section/div/div[2]/section[1]/section/div/div/div[2]/div[5]/div[2]/form/div[2]/div[1]').text
                    flavour_list = list(flavours.splitlines())
                    flavour_list.remove('Flavor')
                    self.product_dict['Flavours'].append(flavour_list)
                except:
                    pass
                
                try:
                    rating = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-68eb7e26-87f6-4711-8408-2327df293f70"]/section/div/div/div/div/span/div[1]/div/div[1]/span').text
                    self.product_dict['Rating'].append(rating)
                except:
                    pass

        def product_id(self, link):
            str(link)
            id = link.replace('https://gorillamind.com/collections/all-products/products/', '')
            self.product_dict['ID'].append(id)
            

        def extract_image(self, link):
            self.driver.get(link)
            image_HTML = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/section/div/div[2]/section[1]/section/div/div/div[1]/div/div[1]/div/div/div[1]/div/img')
            src = image_HTML.get_attribute('src')
            self.product_dict['Image Link'].append(src)
        
        def gen_unique_id(self):
            self.product_dict['UUID'].append(uuid.uuid4())
        
        def make_prod_dict(self, link):
            self.extract_text(link)
            self.extract_image(link)
            self.product_id(link)
            self.gen_unique_id()
            print(self.product_dict)
            


gorilla_mind = GorillaMindScraper('https://gorillamind.com/collections/all?page=1')
gorilla_mind.make_prod_dict('https://gorillamind.com/collections/all/products/gorilla-mode')

