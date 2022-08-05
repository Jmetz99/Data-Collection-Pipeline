from math import prod
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GorillaMindScraper:
    if __name__ == "__main__":
        def __init__(self):
            self.url = 'https://gorillamind.com/collections/all?page=1'
            chrome_options = Options()
            self.driver = webdriver.Chrome(options=chrome_options)
            
        def open_page(self):
            self.driver.get(self.url)

        def get_links(self):
            prod_container = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]')
            prod_list = prod_container.find_elements(by=By.XPATH, value = './div')
            link_list = []
            for product in prod_list:
                a_tag = product.find_element(by=By.TAG_NAME, value='a')
                link = a_tag.get_attribute('href')
                link_list.append(link)
            print(link_list)
            return link_list
            

        def click_product(self):
            product = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/a')
            product.click()
            pass

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
            dict_products = {'Name': [], 'Price': [], 'Description': [], 'Flavours': [], 'Rating': []}

            name = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/h1').text
            dict_products['Name'].append(name)

            price = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/p').text
            dict_products['Price'].append(price)

            description = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[2]/div/div/div[1]/div/div[1]/div[1]/span[1]').text
            dict_products['Description'].append(description)

            flavours = self.driver.find_element(by=By.XPATH, value='//*[@id="product_form_4898112667693"]/div[2]/div[1]').text
            flavour_list = list(flavours.splitlines())
            flavour_list.remove('Flavor')
            dict_products['Flavours'].append(flavour_list)

            rating = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-68eb7e26-87f6-4711-8408-2327df293f70"]/section/div/div/div/div/span/div[1]/div/div[1]/span').text
            dict_products['Rating'].append(rating)

            return dict_products

        def extract_image(self, link):
            self.driver.get(link)
            image_HTML = self.driver.find_element(by=By.XPATH, value='//*[@id="21549905936429"]')
            src = image_HTML.get_attribute('src')
            print(src)




gorilla_mind = GorillaMindScraper()
prod_info = gorilla_mind.extract_text("https://gorillamind.com/collections/all/products/gorilla-mode")

