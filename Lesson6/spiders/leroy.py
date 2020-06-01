# -*- coding: utf-8 -*-
import scrapy
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self,text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        ads_links = response.xpath("//a[contains(@class,'product-name-inner')]/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        yield response.follow(next_page, callback=self.parse)

    def parse_ads(self,response):
        loader = ItemLoader(item=LeroyparserItem(),response=response)
        loader.add_xpath('name','//h1/text()')
        loader.add_xpath('price',"//meta[@itemprop='price']/@content")
        loader.add_xpath('currency',"//meta[@itemprop='priceCurrency']/@content")
        loader.add_xpath('photo',"//picture/source[@itemprop='image']/@data-origin")
        loader.add_xpath('props',"//section[@id='nav-characteristics']")
        loader.add_value('link',response.url) # тут можно былобы взять тег canonical или id product из meta ещё чтобы избежать дублей
        yield loader.load_item()


        # name = response.xpath('//h1/span/text()').extract_first()
        # photo = response.xpath("//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url").extract()
        # yield AvitoparserItem(name=name, photo=photo)