from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['news']
news = db.news

url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

response = requests.get(url, headers)
dom = html.fromstring(response.text)
items = dom.xpath("//section[contains(@class, 'b-top7-for-main')]/div[@class='span4']/div[@class='first-item']/h2"
                  "//section[contains(@class, 'b-top7-for-main')]/div[@class='span4']/div[@class='item']")

items_list = []
for item in items:
    items_data = {}
    source_news = url
    datetime = item.xpath(".//time[@class='g-time']//@datetime")[0]
    name = item.xpath("./a/text()")[0]
    link = item.xpath("./a/@href")[0]
    if link[0] == '/':
        link = f'{url} + {link}'

    items_data['source_news'] = source_news
    items_data['name'] = name
    items_data['link'] = link
    items_data['datetime'] = datetime
    items_list.append(items_data)
    news.update_one({'name': items_data['name']}, {'$set': items_data}, upsert=True)

for item in news.find({}):
    pprint(item)
