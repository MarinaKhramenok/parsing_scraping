# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from urllib.parse import urlparse

from itemadapter import ItemAdapter
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class InstagramPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram09

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        print()
        return item


class InstagramImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            try:
                yield scrapy.Request(item['photos'], meta=item)
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None, *, item):
        return f'images/{item["name"]}' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item