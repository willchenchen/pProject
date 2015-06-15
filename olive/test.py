#!/usr/bin/env python
# encoding: utf-8

import re

x=u'''求搬走， 搬家卖电脑桌,电视柜￥10<div><br/> 小电脑桌铁木各一个$10,电视柜$10，只求搬走， 给钱不给钱都拿走搬走，近MQ大学MARSFIELD自取,孰不能送货,请电/微信:0414360912,QQ:1042134173  <br /> </div>div>'''

index=x.find(u'送货')

if u'不' in x[index-5:index]:
    print x.find(u'送货')
