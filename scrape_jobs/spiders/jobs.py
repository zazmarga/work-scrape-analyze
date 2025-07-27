import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/"]

    def parse(self, response):
        pass
