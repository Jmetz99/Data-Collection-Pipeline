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
            self.open_page()
            self.get_links()
            self.scroll_to_next_page_button()
            self.close_offer()
            self.go_to_next_page()
            
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
            time.sleep(4)
            close_button = self.driver.find_element(by=By.XPATH, value='//*[@id="SMSBump-Modal"]/div/div/button')
            close_button.click()

        def go_to_next_page(self):
            next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
            next_page.click()

gorilla_mind = GorillaMindScraper()

