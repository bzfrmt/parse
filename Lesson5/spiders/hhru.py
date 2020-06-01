# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, vacansy):
        self.start_urls = [f'https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text={vacansy}&fromSearch=true']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        job_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in job_links:
            yield response.follow(link, callback=self.vacansy_parse)
        yield response.follow(next_page, callback=self.parse)


    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = ' '.join(response.xpath("//p[@class='vacancy-salary']/span/text()").extract())
        yield JobparserItem(name=name,salary=salary)
