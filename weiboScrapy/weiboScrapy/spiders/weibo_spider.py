import scrapy

class weiboSpider(scrapy.spider.Spider):
    name="weiboSpider"
    url="http://www.weibo.com/"
    request_with_headers=Request(url="http://weibo.com/u/5611058982/home"
            headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                'Connection':
                }
            )


