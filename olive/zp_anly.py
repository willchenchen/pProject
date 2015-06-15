#!/usr/bin/env python
# encoding: utf-8

import re
import codecs

def dig_area(temp,dic_area):
    area='null'
    for x in dic_area:
        if temp.find(x.lower())!=-1:
            if area=='null':
                area=x.lower()
            else:
                area=area+','+x.lower()
    return area

def dig_salary(temp,pricekw):
    price='null'
    p=False
    for x in pricekw:
        kwindex=temp.find(x)
        while kwindex!=-1:
            temp1=re.search('[0-9]{2,3}k?',temp[kwindex-5:kwindex+10])
            if temp1!=None:
                price=temp1.group(0)
                p=True
                break
            kwindex=temp.find(x,kwindex+1)
        if p:break
    return price

file1=codecs.open('/home/will/tmp/olive/dic_area.txt','r','utf8')
dic_area={}

for x in file1:
    temp=x.strip('\r\n').split(',')
    if re.search('New South Wales',temp[1])!=None:
        dic_area[temp[0].lower()]='New South Wales'

file2=codecs.open('/home/will/tmp/olive/car/zhaopin.txt','r','utf8')
result=[]
temp=''
while True:
    tempread=file2.read(8192)
    tempread=temp+tempread
    if not tempread:break
    tempread=tempread.split('<#>\r\n')
    temp=tempread.pop()
    for x in tempread:
        t1=x.split('<#>')
        if t1[8]=='null':
            t2=t1[0]+t1[2]
            t1[8]=dig_area(t2.lower(),dic_area)

        salary=[u'$']
        if t1[16]=='null':
            t2=t1[0]+t1[2]
            t1[16]=dig_salary(t2.lower(),salary)

        jobtype=[u'全职',u'兼职']
        if t1[13]=='null':
            t2=t1[0]+t1[2]
            t1[13]=dig_area(t2.lower(),jobtype)

        jobcate=[u'销售',u'司机',u'侍應',u'收銀',u'家政',u'保姆',u'洗碗工',u'粉麵工',u'服务员',u'理货',u'发传单',u'幫鑊',u'油鑊',u'雜工',u'送餐',u'司機',u'幫工',u'收银員',u'理貨',u'sales',u'市场咨询',u'按摩',u'助理',u'杂工',u'代读',u'accountant',u'清洁',u'帮工']
        if t1[14]=='null':
            t2=t1[0]+t1[2]
            t1[14]=dig_area(t2.lower(),jobcate)

        result.append(t1)

write_file=codecs.open('/home/will/tmp/olive/car1/zp.txt','w','utf8')
for x in result:
    write_file.write('<#>'.join(s for s in x)+'<#>\r\n')
