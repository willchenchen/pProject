#!/usr/bin/env python
# encoding: utf-8
'''榜单排名数据(更新)'''
import urllib2
import json
import MySQLdb
import datetime
import codecs

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306
ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()
sql='select distinct appid_or_friendid from actual_completion_table where start_date between date_sub(curdate(),interval 14 day) and date_sub(curdate(),interval 1 day) and classify=0;'
cur.execute(sql)
appId=cur.fetchall()

result=[]
sql='select date,genreId,popId,appids from list_rank_cn_table where date between date_sub(curdate(),interval 14 day) and date_sub(curdate(),interval 1 day) and popId in (27,30);'
cur.execute(sql)
try:
    for x in cur.fetchall():
        temp=x[3].split(',')
        for y in appId:
            if y[0] in temp:
                result.append([x[0],str(x[1]),str(x[2]),y[0],str(temp.index(y[0])+1)])
except IndexError:
    pass
ctd.close()

with codecs.open('/Users/will/myData/acc_appid4.txt','w','utf-8') as wf:
    for x in result:
        wf.write('\t'.join(s for s in x)+'\n')

