#!/usr/bin/env python
# encoding: utf-8
'''查询活跃商户数'''
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
sql="select date_sub(curdate(),interval %d day),date_sub(curdate(),interval %d day),count(distinct appid_or_friendid),count(user_id) from actual_completion_table where date between date_sub(curdate(),interval %d day) and date_sub(curdate(),interval %d day) and classify=0;"
i=1
result=[]
while(True):
    cur.execute(sql%(i+6,i,i+6,i))
    temp=cur.fetchone()
    print i,i+6,temp,int(temp[2])
    if int(temp[2])!=0 and temp[0]>=datetime.date(2014,10,1):
        result.append([temp[0],temp[1],int(temp[2]),int(temp[3])])
        i+=7
    else:
        break
ctd.close()

with codecs.open('/Users/will/myData/acc_appid1.txt','w','utf-8') as wf:
    for x in result:
        wf.write(str(x[0])+'\t'+str(x[1])+'\t'+str(x[2])+'\t'+str(x[3])+'\n')
