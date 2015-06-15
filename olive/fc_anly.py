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

def dig_rent(temp,pricekw):
    price='null'
    p=False
    for x in pricekw:
        kwindex=temp.find(x)
        while kwindex!=-1:
            temp1=re.search('[0-9]{3}',temp[kwindex-5:kwindex+10])
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

file2=codecs.open('/home/will/tmp/olive/car/chuzu.txt','r','utf8')
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

        pricekw=[u'$',u'刀',u'单人',u'双人',u'rent',u'租金',u'房租',u'per',u'全包',u'一周',u'/人',u'room',u'每周',u'/周',u'bill',u'/w',u'1人']
        if t1[9]=='null':
            t2=t1[0]+t1[2]
            t1[9]=dig_rent(t2.lower(),pricekw)

        result.append(t1)
write_file=codecs.open('/home/will/tmp/olive/car1/fc.txt','w','utf8')
for x in result:
    write_file.write('<#>'.join(s for s in x)+'<#>\r\n')

