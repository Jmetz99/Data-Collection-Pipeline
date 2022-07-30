from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, url):
        self.url = url
        
    def open_page(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def scroll_page(self):
        self.open_page()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def go_to_next_page(self):
        self.scroll_page()
        next_page = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-collection__main"]/div/div[2]/div/div/nav/a')
        next_page.click()
    
    def click_random_product(self):
        self.open_page()
        product

