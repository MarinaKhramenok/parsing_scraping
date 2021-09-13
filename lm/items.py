# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    value_clear = value.replace(' ', '')
    try:
        return int(value_clear)
    except:
        return value

def process_info(value):
    value_clear = value.replace('\n                ', '').replace('\n            ', '')
    return value_clear

class LmItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    item_term = scrapy.Field()
    item_details = scrapy.Field(input_processor=MapCompose(process_info))
    item_info = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
