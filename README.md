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
In this milestone I implemented some further tests for the public methods in my scraper. For example, I tested the 'click_object()' method actually interacts with the element it is given. I also used moto to mock amazon s3 services, allowing me to test whether my 'upload_to_s3()' method actually stored data in an s3 bucket. 

In order to prevent rescraping data, I implemented a method which queries my aws RDS for all the existing product ID's and compares these with the set of links to scrape to find the symmetric difference, i.e. the links which haven't been scraped.

## Milestone 8
In this milestone I learnt to use docker to containerise my application and run it successfully on an ec2 instance. By generating a docker image, pushing this to dockerhub, pulling it onto the ec2 and running it there.

## Milestone 9
In this milestone I ran prometheus, an open-source software for monitoring and alerting, on my EC2 instance to track metrics from prometheus itself, the operating system and docker. With the data outputted from prometheus I created a grafana dashboard to present these metrics in a accessible format.

## Milestone 10
