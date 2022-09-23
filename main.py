from operator import concat
from utils.scraper import Scraper
from sqlalchemy import create_engine
import pandas as pd
import os
import psycopg2
import numpy as np
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'gorilla.cjzhidft7nnj.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = os.environ.get('Password')
DATABASE = 'postgres'
PORT = 5432
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
engine.connect()

if __name__ == '__main__':
    scraper = Scraper()
    scraper.driver.get('https://gorillamind.com/products/gorilla-mode')
    image_link = scraper.extract_image_link()
    print(image_link)
    scraper.driver.quit()