import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[contains(@class, 'icMQ_')]/@href").getall()
        next_page = response.xpath("//span[contains(text(), 'Дальше')]").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow('https://superjob.ru' + link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        v_name = response.xpath("//h1/text()").get()
        v_salary = response.xpath("//span[contains(@class, '_1OuF_ ZON4b')]//text()").getall()
        v_url = response.url
        yield JobparserItem(name=v_name, salary=v_salary, url=v_url)
