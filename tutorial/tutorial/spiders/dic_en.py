#!/usr/bin/env python
# encoding: utf-8

import scrapy
import codecs

class EngSpider(scrapy.Spider):
    name="en_spider"
    allowed_domanis=['wiktionary.org']
    start_urls =["http://en.wiktionary.org/wiki/Appendix:List_of_the_1750_most_frequently_used_French_words"]

    wf=codecs.open("/home/will/data/fre_dic.txt",'w','utf8')

    def parse(self, response):
        result=[]
        for sel in response.xpath("//ul/li/a|//p/a"):
            result.extend(sel.xpath('text()').extract())
        print len(result)
        self.wf.write('\n'.join(s for s in result if s!=" "))

