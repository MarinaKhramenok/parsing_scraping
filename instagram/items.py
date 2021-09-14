# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    followers = scrapy.Field()
    subs_type = scrapy.Field()
    photos = scrapy.Field()
    main_user = scrapy.Field()
