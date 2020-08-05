import scrapy


class GetrealestateSpider(scrapy.Spider):
    name = 'getRealEstate'
    allowed_domains = ['https://www.idealista.com/']
    start_urls = ['http://https://www.idealista.com//']

    def parse(self, response):
        pass
