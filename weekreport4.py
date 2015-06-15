#!/usr/bin/env python
# encoding: utf-8
'''榜单排名数据'''
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
result=[]
for x in cur.fetchall():
    url='http://api.asou.com/JsonData/bgRankValue?country=cn&'
    url=url+'appid='+str(x[0])+'&'
    for y in range(14):
        td=datetime.date.today()-datetime.timedelta(y+1)
        url1=url+'time='+str(td)
        req=urllib2.Request(url1)
        f=urllib2.urlopen(req)
        temp=json.loads(f.read())
        for z in temp.values()[0]:
            if z['popId'] in (str(27),str(30),str(38)):
                row=[]
                print z
                row.append(td)
                row.append(z['appid'])
                row.append(z['popId'])
                row.append(z['genreId'])
                row.append(z['appName'])
                row.append(z['popRank'])
                result.append(row)
ctd.close()

with codecs.open('/Users/will/myData/acc_appid4.txt','w','utf-8') as wf:
    for x in result:
        wf.write(str(x[0])+'\t'+str(x[1])+'\t'+str(x[2])+'\t'+str(x[3])+'\t'+x[4]+'\t'+str(x[5])+'\n')
