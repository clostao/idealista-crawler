import scrapy
from ..static_data import get_provincies

class GetareasSpider(scrapy.Spider):
    name = 'getRealEstate'
    allowed_domains = ['https://www.idealista.com/']
    real_estate_types = ["venta-trasteros", "venta-garajes"]
    start_urls = get_provincies(self.real_estate_types)


    def parse(self, response, region=""):
        if (region == ""):
            tab = response.url.split("/")
            region = tab[len(tab) - 2]
        selector = Selector(response)
        elements = selector.css("#sublocations li a")
        sublocations = elements.xpath("@href").extract()
        sublocation_names = elements.xpath("text()").extract()
        if (len(sublocations) > 0):
            for i, sublocation in enumerate(sublocations):
                yield Request(url=(self.base_url + sublocation), callback=self.parse, cb_kwargs={'region':(region + ">" + sublocation_names[i])})
        else:
            product_links = selector.css("a.item-link").xpath("@href").getall()
            for product_link in product_links:
                yield Request(url=(self.base_url + product_link),callback=self.parse_area_page,cb_kwargs={'region':region})
            next_button = selector.css("li.next > a").xpath("@href").get()
            if next_button:
                yield Request(url=(self.base_url + next_button), callback=self.parse_area_page, cb_kwargs={'region':region})
            
    def parse_area_page(self, response, region):
        selector = Selector(response)
        product_links = selector.css("a.item-link").xpath("@href").getall()
        for product_link in product_links:
            yield Request(url=(self.base_url + product_link), callback=self.parse_real_estate, cb_kwargs={'region':region})
        next_button = selector.css("li.next > a").xpath("@href").get()
        if next_button:
            yield Request(url=(self.base_url + next_button), callback=self.parse_area_page, cb_kwargs={'region':region})
    def parse_real_estate(self, response, region):
        selector = Selector(response)
        price = selector.css("info-data-price span.txt-bold").xpath("text()").get()
        size = selector.css("div.info-features>span").xpath("text()").get()
        floor = selector.css("div.info-features>span + span + span").xpath("text()").get()
        item = ItemLoader(RealEstate(), selector)
        item.add_value("uid", get_uid_from_link(response.url))
        item.add_value("price", price)
        item.add_value("size", size)
        item.add_value("floor", floor)
        item.add_value("region", region)
        yield item.load_item()

def get_uid_from_link(url):
    tab = url.split("/")
    return (tab[len(tab) - 2])
