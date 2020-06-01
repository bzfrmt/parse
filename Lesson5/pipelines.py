# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import re
#import urlparse


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacansy_330

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class JobparserPipelineSalary:


    def process_item(self, item, spider):
        item['salary'] = re.sub('<[^>]+?>', '', item['salary'].replace('\xa0',''))
        item['minsalary'] = None
        item['maxsalary'] = None
        item['currency'] = None
        #item.host = urlparse.urlparse('http://ngs.pradhi.com/upload')['netloc']

        if spider.name == 'hhru':
            item['host']='hh.ru'
            salary = {}
            salary=re.search("(\d+)\s*\-\s*(\d+)\s+(\D+)", item['salary'])
                if salary:
                    #print('val:',salary[3],' min:',salary[1],'max:',salary[2])
                    item['currency'] = salary[3]
                    item['minsalary'] = salary[1]
                    item['maxsalary'] = salary[2]

            salary=re.search("от\s+(\d+)\s+(\D+)", item['salary'])
                if salary:
                    #print('val:',salary[2],' min:',salary[1])
                    item['currency'] = salary[2]
                    item['minsalary'] = salary[1]

            salary=re.search("до\s+(\d+)\s+(\D+)", item['salary'])
                if salary:
                    #print('val:',salary[2],' max:',salary[1])
                    item['currency'] = salary[2]
                    item['maxsalary'] = salary[1]

            salary=re.search("^(\d+)\s+(\D+)", item['salary'])
                if salary:
                    #print('val:',salary[2],' max:',salary[1])
                    item['currency'] = salary[2]
                    item['minsalary'] = salary[1]
                    item['maxsalary'] = salary[1]


        if spider.name == 'sjru':
            item['host']='superjob.ru'
            salary = {}
            salary=re.search("^(\d+)\s*(\D+)", item['salary'])
                if salary:
                        #print('val:',salary[2],' max:',salary[1])
                    item['currency'] = salary[2]
                    item['minsalary'] = salary[1]
                    item['maxsalary'] = salary[1]
            salary=re.search("(\d+)\s*\—\s*(\d+)\s*(\D+)", item['salary'])
                if salary:
                        #print('val:',salary[3],' min:',salary[1],'max:',salary[2])
                    item['currency'] = salary[3]
                    item['minsalary'] = salary[1]
                    item['maxsalary'] = salary[2]

            salary=re.search("от\s*(\d+)\s*(\D+)", item['salary'])
                if salary:
                        #print('val:',salary[2],' min:',salary[1])
                    item['currency'] = salary[2]
                    item['minsalary'] = salary[1]

            salary=re.search("до\s*(\d+)\s*(\D+)", item['salary'])
                if salary:
                        #print('val:',salary[2],' max:',salary[1])
                    item['currency'] = salary[2]
                    item['maxsalary'] = salary[1]

        return item



