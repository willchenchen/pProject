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

def dig_brand(temp,car_brand):
    brand='null'
    for x in car_brand:
        kwindex=temp.find(x)
        if kwindex!=-1 and u'不' not in temp[kwindex-5:kwindex]:
            brand=x
            break
    return brand

def dig_prod(temp,dic_area):
    area='null'
    area1='null'
    for i,x in dic_area.iteritems():
        if temp.find(i.lower())!=-1:
            if area=='null':
                area=i.lower()
                area1=x.lower()
            else:
                area=area+','+i.lower()
    return (area,area1)

file1=codecs.open('/home/will/tmp/olive/dic_area.txt','r','utf8')
dic_area={}
for x in file1:
    temp=x.strip('\r\n').split(',')
    if re.search('New South Wales',temp[1])!=None:
        dic_area[temp[0].lower()]='New South Wales'

file3=codecs.open('/home/will/tmp/olive/dic_es.txt','r','utf8')
es_prod={}
for x in file3:
    temp=x.strip('\r\n').split('\t')
    es_prod[temp[0]]=temp[1]

file2=codecs.open('/home/will/tmp/olive/car/shangpin.txt','r','utf8')
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
        t2=t1[0]+t1[2]
        if t1[8]=='null':
            t1[8]=dig_area(t2.lower(),dic_area)

        is_delivery=[u'送货']
        if t1[17]=='null':
            t1[17]=dig_brand(t2.lower(),is_delivery)

        if t1[16]=='null':
            t=dig_prod(t2.lower(),es_prod)
            t1[16]=t[0]
            t1[15]=t[1]
            if t1[16]!='null':print t2,t1[16]

        result.append(t1)

write_file=codecs.open('/home/will/tmp/olive/car1/es.txt','w','utf8')
for x in result:
    write_file.write('<#>'.join(s for s in x)+'<#>\r\n')

