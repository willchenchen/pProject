#!/usr/bin/env python
# encoding: utf-8
'''上榜数据情况'''
import MySQLdb
import datetime
import codecs

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306

ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
sql="select date,appid_or_friendid,keywords,count(user_id) from actual_completion_table where date between date_sub(curdate(),interval 7 day) and date_sub(curdate(),interval 1 day) and classify=0 group by date,appid_or_friendid,keywords;"
cur=ctd.cursor()
cur.execute(sql)
kw_down=[]
for x in cur.fetchall():
    kw_down.append([x[0],int(x[1]),x[2].lower(),int(x[3])])
sql="select distinct date,keywords,hints from hints_table_trendsonly where date between date_sub(curdate(),interval 7 day) and date_sub(curdate(),interval 1 day) and rank<=10;"
cur.execute(sql)
hitswd=[]
for x in cur.fetchall():
    hitswd.append([x[0],x[1].lower(),x[2]])
ctd.close()

result=[]
for x in kw_down:
    d=False
    for y in hitswd:
        if x[2]==y[1] and x[0]<=y[0] and x[0]>=y[0]-datetime.timedelta(1):
            result.append(x+[y[0],y[2]])
            d=True
    if d==False:
        result.append(x+[d,d])

with codecs.open('/Users/will/myData/acc_appid2.txt','w','utf8') as wf:
    for x in result:
        wf.write(str(x[0])+'\t'+str(x[1])+'\t'+x[2]+'\t'+str(x[3])+'\t'+str(x[4])+'\t'+str(x[5])+'\n')
