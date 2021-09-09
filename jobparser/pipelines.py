# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy09

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_sjru(item['salary'])
        item['source'] = spider.name
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        try:
            salary = salary.replace('\u202f', '')
            salary = salary.replace('\xa0', '')
            currency = salary.split()[-1]
            if salary == [''] or salary == ['По договорённости'] or salary == []:
                currency = None
                min_salary = None
                max_salary = None
            if 'от' in salary and 'до' in salary:
                min_salary = int(salary.split(' ')[1])
                max_salary = int(salary.split(' ')[3])
            elif 'от' in salary:
                min_salary = int(salary.split(' ')[1])
                max_salary = None
            elif 'до' in salary:
                min_salary = None
                max_salary = int(salary.split(' ')[2])
            elif currency == 'указана':
                min_salary, max_salary, currency = None

        except:
            min_salary, max_salary, currency = None

        return min_salary, max_salary, currency

    def process_salary_sjru(self, salary):
        try:
            salary = ''.join(salary)
            salary = salary.replace('\u202f', '')
            currency = salary.split[-1]

            if '—' in salary:
                min_salary = int(salary[0])
                max_salary = int(salary[4])
            elif 'от' in salary:
                min_salary = int(salary.split[2])
                max_salary = None
            elif 'до' in salary:
                min_salary = None
                max_salary = int(salary.split[2])
            else:
                min_salary, max_salary, currency = None
        except:
            min_salary, max_salary, currency = None, None, None
        return min_salary, max_salary, currency