# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.avito_ads_330

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroyPhotoPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        print(1)
        return item

    #не совсем понятно какой  url?
    #предполагаю что это урл скачиваемого изображения. пытаюсь из урла вытащить id продукта и создать с таким id папочку для изображений
    def file_path(self, request, response=None, info=None):
        filepath = 'full/'
        key = re.search('\/(\d+)_\d+\.(?:jpg|jpeg|png|gif)$',request.url)
        if key:
            filepath=filepath + key[1] + '/'
        return filepath


