# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacansy):
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={vacansy}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        job_links = re.findall('<a[^>]*?icMQ[^>]*?(\/vakansii\/[^>\/"]*?\-\d+\.html)[^>]*>(.+?)<\/a>',response.text)
        if job_links:
            for link in job_links:
                yield response.follow(link[0], callback=self.vacansy_parse)
        yield response.follow(next_page, callback=self.parse)


    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = ' '.join(response.xpath("//span[contains(@class,'_3mfro _2Wp8I ZON4b PlM3e _2JVkc')]/text()").extract())
        yield JobparserItem(name=name,salary=salary)
