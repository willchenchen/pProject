#!/usr/bin/env python
# encoding: utf-8
'''查询累计服务apps数'''
import MySQLdb
import codecs
import datetime

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306
ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()
sql="select date_sub(curdate(),interval %d day),count(distinct appid_or_friendid) from actual_completion_table where date<=date_sub(curdate(),interval %d day) and classify=0;"
i=1
result=[]
while(True):
    cur.execute(sql%(i,i))
    temp=cur.fetchone()
    print i,temp,int(temp[1])
    if int(temp[1])!=0 and temp[0]>=datetime.date(2014,10,1):
        result.append([temp[0],int(temp[1])])
        i+=7
    else:
        break
ctd.close()

with codecs.open('/Users/will/myData/acc_appid.txt','w','utf-8') as wf:
    for x in result:
        wf.write(str(x[0])+'\t'+str(x[1])+'\n')
