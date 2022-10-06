from utils.scraper import Scraper
import os
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
DATABASE_TYPE = 'postgresql'
PORT = 5432
engine = create_engine(f"{DATABASE_TYPE}+{'psycopg2'}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
engine.connect()

if __name__ == '__main__':
    scraper = Scraper()
    new_data = scraper.scrape_all_data()
    new_data.to_sql(name='gorilla', con=engine, if_exists = 'append', index=False)
    