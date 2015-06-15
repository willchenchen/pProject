#!/usr/bin/env python
# encoding: utf-8

import scrapy

class garyspider(scrapy.Spider):
    name='dic_area'
    allowed_domains='http://en.wikipedia.org/wiki'

    def start_requests(self):
        yield scrapy.FormRequest("http://en.wikipedia.org/wiki/List_of_Sydney_suburbs",callback=self.parse)

    def parse(self, response):
        filename = response.url.split("/")[-1]
        result=[]
        for sel in response.xpath("//div[@id='mw-content-text']/p"):
            result.extend(sel.xpath('a/@title').extract())

        with open(filename, 'a') as f:
            for s in result:
                f.write(s+'\r\n')
