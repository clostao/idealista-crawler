# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlidealistaItem(scrapy.Item):
    uid = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    floor = scrapy.Field()
    region = scrapy.Field()
    pass
