#!/usr/bin/env python
# encoding: utf-8

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

class TestSpider(CrawlSpider):
    name = "test"
    domain_name = "http://www.sydneytoday.com/"
    start_urls = ["http://www.sydneytoday.com/"]
    def parse(self, response):
        open('test.html', 'wb').write(response.body)
