# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeJobsItem(scrapy.Item):
    job_id = scrapy.Field()
    job_url = scrapy.Field()
    title = scrapy.Field()
    job_data = scrapy.Field()
    requirements = scrapy.Field()

