#!/usr/bin/env python
# encoding: utf-8

import MySQLdb
import urllib2
import urllib
import json
import codecs

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306
ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()
sql="select date,keywords,count(user_id) from actual_completion_table where date between '2014-12-01' and '2014-12-25' and classify=0 group by date,keywords"
cur.execute(sql)
d={}
opner=urllib2.build_opener()
for x in cur.fetchall():
    d[str(x[0])+'|'+x[1]]=[x[2]]

sql="select date,keywords,avg(hits) from keywords_hits_table where date between '2014-12-01' and '2014-12-25' and country='cn' group by date,keywords"
cur.execute(sql)
d1={}
for x in cur.fetchall():
    d1[str(x[0])+'|'+x[1]]=x[2]

for x in d:
    if x in d1:
        t=x.split('|')
        url=urllib.quote_plus(t[1].encode('utf-8'))
        url="http://c.xn--uur.org:22222/api.priority.php?cc=cn&dev=iphone&kw="+url
        opner=urllib2.urlopen(url)
        r=opner.read()
        r=json.loads(r)
        d[x].append(r["priority"])
print d

write_file=codecs.open('/home/will/data/temp4.txt','w','utf8')
for i,x in d.iteritems():
    temp=i.split('|')
    try:
        write_file.write(temp[0]+'\t'+temp[1]+'\t'+str(x[0])+'\t'+str(x[1])+'\n')
    except IndexError:
        pass


'''
opner=urllib2.build_opener()
url=urllib.quote_plus("抢票神器")
url="http://c.xn--uur.org:22222/api.priority.php?cc=cn&dev=iphone&kw="+url
opner=opner.open(url)
r=opner.read()
r=json.loads(r)
print r["priority"]
'''
