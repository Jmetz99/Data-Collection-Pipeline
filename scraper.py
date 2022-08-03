from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common import service
from selenium.webdriver.chrome.options import Options


class GorillaMindScraper:
    if __name__ == "__main__":
        def __init__(self):
            self.url = 'https://gorillamind.com/collections/all?page=1'
            chrome_options = Options()
            self.driver = webdriver.Chrome(options=chrome_options)


            
        def open_page(self):
            self.driver.get(self.url)

        def scroll_page(self):
            self.open_page()
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        def go_to_next_page(self):
            self.scroll_page()
            next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
            next_page.click()
        
        def click_product(self):
            self.open_page()
            product = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]/div[4]/div/div[1]/div[2]/a')
            product.click()
        
        def get_links(self):
            self.open_page()
            prod_container = self.driver.find_element(by=By.XPATH, value = '//*[@id="shopify-section-collection__main"]/div/div[1]/div[2]')
            prod_list = prod_container.find_elements(by=By.XPATH, value = './div')
            link_list = []
            for product in prod_list:
                a_tag = product.find_element(by=By.TAG_NAME, value='a')
                link = a_tag.get_attribute('href')
                link_list.append(link)
            return link_list

gorilla_mind = Scraper()

#gorilla_mind_prods = gorilla_mind.get_links()

products = gorilla_mind.get_links()

print(products)
