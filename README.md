# Data-Collection-Pipeline
2nd AiCore project on the data collection pipeline
## Milestone 1, 2 & 3
Created a gorillamind scraper class which, using selenium, can navigate the page, close offer pop ups, and gather a list of links to the gorilla mind products.

## Milestone 4
Stored data collected from scraper in dictionary. Wrote code which saves this dictionary in a folder for each product along with the product image.

## Milestone 5
Wrote unittests for the methods of the scraper concerned with gathering the links to product pages, gathering the data from these pages and correctly storing it.

## Milestone 6
Uploaded raw data of product information in json format and image jpeg to amazon S3. Formatted product data contained in dictionary using pandas and, using sqlalchemy to create an engine linked with AWS database, added product data to the cloud.

## Milestone 7