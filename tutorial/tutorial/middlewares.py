#!/usr/bin/env python
# encoding: utf-8

#import base64

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8118"
        # proxy_user_pass = "willchen:qweasd123"
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

