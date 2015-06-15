#!/usr/bin/env python
# encoding: utf-8

import MySQLdb
import codecs

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306

ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()
sql='select distinct package_name,appid,name from app_info_cn where appid is not null and package_name is not null and name is not null;'
pkg_app={}
cur.execute(sql)
for x in cur.fetchall():
    if x[0] not in pkg_app:
        pkg_app[x[0]]=[x[1],x[2]]
    else:
        print "包名重复"

sql='select distinct user_id,appid_or_friendid from actual_completion_table where classify=0;'
userid_appid={}
cur.execute(sql)
for x in cur.fetchall():
    if x[0] not in userid_appid:
        userid_appid[x[0]]=[x[1]]
    else:
        userid_appid[x[0]].append(x[1])

sql='select distinct user_id,package_name from fs_user_package where user_id is not null and package_name is not null;'
userid_pkg=[]
unfd_pkg=set()
cur.execute(sql)
for x in cur.fetchall():
    if x[0] in userid_appid:
        if x[1] in pkg_app:
            if pkg_app.get(x[1])[0] not in userid_appid.get(x[0]):
                userid_pkg.append([x[0]].extend(pkg_app.get(x[1])))
        else:
            unfd_pkg.add(x[1])
    else:
        if x[1] in pkg_app:
            userid_pkg.append([x[0]].extend(pkg_app.get(x[1])))
        else:
            unfd_pkg.add(x[1])

result=zip(*userid_pkg)
print len(result)

