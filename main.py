from utils.gorilla_mind_scraper import GorillaMindScraper

if __name__ == '__main__':
    scraper = GorillaMindScraper()
    #gorilla_mind_df = pd.DataFrame(all_data)
    # gorilla_mind_df = pd.read_csv('gorilla_mind_df.csv')
    
    # DATABASE_TYPE = 'postgresql'
    # DBAPI = 'psycopg2'
    # HOST = 'aicore-scraper-data.cjzhidft7nnj.eu-west-2.rds.amazonaws.com'
    # USER = 'postgres'
    # PASSWORD = os.environ.get('Password')
    # DATABASE = 'GorillaMindProductData'
    # PORT = 5432
    # engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    # engine.connect()
    
    # with psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DATABASE, port=5432) as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("""SELECT table_name FROM information_schema.tables
    #     WHERE table_schema = 'public'""")
    #         for table in cur.fetchall():
    #             print(table)

    # gorilla_mind_df.to_sql('GorillaMindProductData', engine, if_exists='replace')