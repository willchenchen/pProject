#!/usr/bin/env python
# encoding: utf-8

import scrapy

class garyspider(scrapy.Spider):
    name='gary'
    allowed_domains='http://bbs.tigtag.com'

    def start_requests(self):
        for x in range(10):
            yield scrapy.FormRequest("http://bbs.tigtag.com/forum-48-%s.html"%(x+1),
                    callback=self.parse)

    def parse(self, response):
        filename = response.url.split("/")[-2]

        result=[]
        for sel in response.xpath("//tbody[starts-with(@id,'normalthread')]/tr/th[@class='new']"):
            result.extend(sel.xpath('a/@href').extract())

        with open(filename, 'a') as f:
            for s in result:
                f.write(s+'\r\n')

