import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lm.items import LmItem

class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'http://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        page_links = response.xpath("//a[@data-qa-pagination-item='right']")
        for page in page_links:
            yield response.follow(page, callback=self.parse)

        ads_links = response.xpath("//div[@data-qa-product]/a")
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LmItem(),
                            response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_xpath('price', "////span[@slot='price']/text()")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_xpath('unit', "//span[@slot='unit']/text()")
        loader.add_xpath('item_term', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('item_details', "//dd[@class='def-list__definition']/text()")
        loader.add_value('url', response.url)
        yield loader.load_item()
