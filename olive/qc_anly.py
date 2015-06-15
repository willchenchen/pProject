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
            temp1=re.search(ur'[0-9]+,?[0-9]+k?',temp[kwindex:kwindex+10])
            if temp1!=None:
                price=temp1.group(0)
                p=True
                break
            kwindex=temp.find(x,kwindex+1)
        if p:break
    return price

def dig_brand(temp,car_brand):
    brand='null'
    for x in car_brand:
        kwindex=temp.find(x)
        if kwindex!=-1:
            brand=x
            break
    return brand

def dig_mile(temp,pricekw):
    price='null'
    p=False
    for x in pricekw:
        kwindex=temp.find(x)
        while kwindex!=-1:
            temp1=re.search(ur'[0-9]+,?[0-9]+(k,w,万)?',temp[kwindex-10:kwindex+1])
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

file3=codecs.open('/home/will/tmp/olive/car/汽车估价数据.txt','r','utf8')
car_brand={}
for x in file3:
    temp=x.strip('\r\n').split('<#>')
    if temp[0] not in car_brand:
        car_brand[temp[0].lower()]=[temp[1].lower()]
    else:
        car_brand[temp[0].lower()].append(temp[1].lower())

file2=codecs.open('/home/will/tmp/olive/car/car.txt','r','utf8')
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

        salary=[u'$',u'价格',u'售价']
        if t1[11]=='0.0':
            t1[11]=dig_salary(t2.lower(),salary)

        if t1[9]=='null':
            t1[9]=dig_brand(t2.lower(),car_brand)

        transmission=[u'手自一体',u'手动',u'自动',u'auto',u'manu']
        if t1[17]=='null':
            t1[17]=dig_brand(t2.lower(),transmission)

        mileage=[u'公里',u'km']
        if t1[18]=='null':
            t1[18]=dig_mile(t2.lower(),mileage)

        result.append(t1)

write_file=codecs.open('/home/will/tmp/olive/car1/qc.txt','w','utf8')
for x in result:
    write_file.write('<#>'.join(s for s in x)+'<#>\r\n')

