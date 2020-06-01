# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
import scrapy
import json

def getprops(props):
    data={}
    propslist=props.xpath("//div[@class='def-list__group']")
    if propslist:
        for prop in propslist:
            name = prop.xpath('.//dt[@class="def-list__term"]/text()')[0]
            value = prop.xpath('.//dd[@class="def-list__definition"]/text()')[0]
        data[name]=value
    return json.dump(data)

def getprice(price):
    return float(price)

class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(getprice))
    currency = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    props = scrapy.Field(input_processor=Compose(getprops))

