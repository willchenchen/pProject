#!/usr/bin/env python
# encoding: utf-8

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import codecs
import operator

dir_index='/home/will/tmp/search_index'
file1=codecs.open('/home/will/tmp/badresponse.txt','r','utf-8')

look_up=[]

for x in file1.readlines():
    look_up.append(x.strip('\r\n').split('\t')[0])

ix=open_dir(dir_index)

result={}
for x in look_up:
    with ix.searcher() as searcher:
        query=QueryParser("content",ix.schema).parse(x)
        results=searcher.search(query,limit=None)
        for x in results:
            if x.get('cmt_id') not in result:
                result[x.get('cmt_id')]=x.score
            else:
                result[x.get('cmt_id')]=result.get(x.get('cmt_id'))+x.score

result1=sorted(result.items(),key=operator.itemgetter(1),reverse=True)

write_file=codecs.open('/home/will/tmp/result1.txt','w','utf-8')
for x in result1:
    write_file.write(str(x[0])+'\t'+str(x[1])+'\r\n')

for x in result1:
    with ix.searcher() as searcher:
        query=QueryParser("cmt_id",ix.schema).parse(x[0])
        results=searcher.search(query,limit=None)
        for x in results:
            print x.get('content')

