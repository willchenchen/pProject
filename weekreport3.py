#!/usr/bin/env python
# encoding: utf-8
'''查询关键词下的排名'''
from elasticsearch import Elasticsearch
import MySQLdb
import codecs

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306
ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()
sql="select distinct appid_or_friendid,keywords from actual_completion_table where date between date_sub(curdate(),interval 7 day) and date_sub(curdate(),interval 1 day) and classify=0;"
cur.execute(sql)

es=Elasticsearch('http://kkHLGMphuxBVyUJiZqHH:jfvGWczcZcCDVzxBsLRu@115.159.25.211:9200')
result=[]
for x in cur.fetchall():
    query={'query':{'bool':{'must':[]}}}
    query['query']['bool']['must'].append({'range':{'date':{'lte':'2015-02-24','gte':'2015-02-18'}}})
    query['query']['bool']['must'].append({'term':{'word':x[1]}})
    query['query']['bool']['must'].append({'term':{'appid':int(x[0])}})
    temp=es.search(index='apple_search_result_cn_phone',body=query)
    if len(temp['hits']['hits'])!=0:
        for y in temp['hits']['hits']:
            row=[]
            row.append(y['_source']['date'])
            row.append(y['_source']['appid'])
            row.append(y['_source']['word'])
            row.append(y['_source']['rank'])
            result.append(row)
ctd.close()
print result
with codecs.open('/Users/will/myData/acc_appid3.txt','w','utf-8') as wf:
    for x in result:
        wf.write(str(x[0])+'\t'+str(x[1])+'\t'+x[2]+'\t'+str(x[3])+'\n')
