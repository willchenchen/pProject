#!/usr/bin/env python
# encoding: utf-8

import apriori
import codecs

f=codecs.open('/home/will/data/search_result_cn_phone.txt','r','utf-8')

id_word={}
for x in f:
    temp=x.split('\t')
    if len(temp)==4:
        temp1=temp[1].split(',')
        for y in temp1:
            if y not in id_word:
                id_word[y]=[temp[0]]
            else:
                id_word[y].append(temp[0])
'''
with codecs.open('/home/will/data/temp.txt','w','utf-8') as wf:
    for key,value in id_word.iteritems():
        wf.write(str(key)+'\t'+'\t'.join(s for s in value)+'\n')
'''
l,support_data=apriori.apriori(id_word.values(),minSupport=0.001)
print '#########################################################'
print l

