#!/usr/bin/env python
# encoding: utf-8

import codecs
import MySQLdb

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306

ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()
sql='select distinct package_name from fs_user_package where package_name is not null;'
cur.execute(sql)
all_pkg=[]
for x in cur.fetchall():
    all_pkg.append(x[0])

sql='select distinct package_name from app_info_cn where package_name is not null;'
cur.execute(sql)
dic={}
for x in cur.fetchall():
    dic[x[0]]=''

sql='select distinct package_name from app_info_jp where package_name is not null;'
cur.execute(sql)
for x in cur.fetchall():
    dic[x[0]]=''

sql='select distinct package_name from app_info_us where package_name is not null;'
cur.execute(sql)
for x in cur.fetchall():
    dic[x[0]]=''

for i,x in enumerate(all_pkg):
    if x in dic:
        del all_pkg[i]

with codecs.open('/home/will/data/unfd_pkg.txt','w','utf8') as wf:
    wf.write('\n'.join(s for s in all_pkg))



