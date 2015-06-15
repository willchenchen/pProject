#!/usr/bin/env python
# encoding: utf-8

import scrapy
from tutorial1.items import Tutorial1Item

class CpSpider(scrapy.Spider):
    name='haodou'
    allowed_domains=['haodou.com']

    def start_requests(self):
        url='http://www.haodou.com/search/recipe/西式早餐?p=%d&type=list'
        return [scrapy.Request(url%(x+1),callback=self.parse) for x in range(10)]

    def parse(self,response):
        for sel in response.selector.xpath("//ul[@id='the-list']/li/div/p[1]"):
            item=Tutorial1Item()
            item['url']=sel.xpath('a[1]/@href').extract()
            yield item
