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
    new_data = scraper.get_data()
    
    # gorilla_mind_df = scraper.get_all_data()
    # print(gorilla_mind_df)
    # gorilla_mind_df = pd.read_csv('/Users/jacobmetz/Documents/web_scraper/utils/gorilla_mind_df.csv')
    
    # new_ids = pd.DataFrame(gorilla_mind_df["ID"])
    # old_ids = pd.read_sql_query('''SELECT "ID" FROM "GorillaMindProductData"''', engine)
   
    # difference_locations = np.where(new_ids != old_ids)
    # indicies = difference_locations[0].tolist()
    # different_ids = new_ids.values[difference_locations]

    # new_items = gorilla_mind_df.iloc[indicies]
    # new_items = new_items.reset_index(drop=True)
    
