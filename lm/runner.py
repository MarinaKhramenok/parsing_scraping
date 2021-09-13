from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lm.spiders.lmru import LmruSpider
from lm import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmruSpider, query='ковер')
    process.start()