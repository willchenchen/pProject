import scrapy
from stockScrapy.items import StockscrapyItem

class stockIdSpider(scrapy.spider.Spider):
    name="stockId"
    start_urls=["http://quote.eastmoney.com/stocklist.html"]

    def parse(self,response):
        for x in response.selector.css('#quotesearch a[target=_blank]::text').extract():
            item=StockscrapyItem()
            item['stockId']=x
            yield item
            

