#!/usr/bin/env python
# encoding: utf-8

import codecs
import jieba.posseg as pseg
import jieba
import collections
import math

rf=codecs.open('/Users/will/myData/2015-05-04_cn_6015_27.txt','r','utf-8')

tempStr=''
tempDict={}
tempTerm=set()

avoidWord=(u'电脑',u'手机',u'网站',u'集体',u'成员',u'平台',u'终端',u'信息',u'云端',u'服务器',u'经验',u'质量',u'产品',u'个人',u'小企业',u'有限公司',u'用户',u'隶属于',u'来到',u'现已',u'无论是',u'始终',u'等等',u'还是',u'还有',u'使用',u'方式',u'可以',u'打磨',u'声音',u'倾心',u'期待',u'酷炫',u'iPhone',u'独特',u'精心',u'依托',u'优势',u'电子',u'灵活',u'QQ',u'满足',u'需求',u'技术',u'打造',u'我们',u'体验',u'服务',u'操作',u'进行',u'提供',u'众多',u'亿多',u'付宝',u'Windows',u'Mobile',u'iphone',u'数十家',u'其他',u'版本',u'包括',u'成功',u'一个',u'研发',u'IT',u'浪潮')
while True:
    rdStr=tempStr+rf.read(1024)
    if rdStr:
        temp=rdStr.split('@@@|||@@@\r\n')
        tempStr=temp.pop()
        for x in temp:
            temp1=x.split('\t@@@|||@@@')
            temp2=[]
            for s in jieba.cut(temp1[1]):
                if len(s)>1 and s not in avoidWord:
                    temp2.append(s)
                    tempTerm.add(s)
            tempDict[temp1[0]]=collections.Counter(temp2)
    else:
        break
rf.close()

lenDict=len(tempDict)
tfidf={}
for x in tempTerm:
    lenTerm=0
    for v in tempDict.itervalues():
        if x in v:
            lenTerm+=1
    for k,v in tempDict.iteritems():
        if k not in tfidf and x in v:
            temp=float(v.get(x))/sum(v.values())*math.log(lenDict/lenTerm)
            tfidf[k]={x:temp}
        if k in tfidf and x in v:
            temp=float(v.get(x))/sum(v.values())*math.log(lenDict/lenTerm) 
            tfidf[k][x]=temp

with codecs.open('/Users/will/myData/test.txt','w','utf-8') as wf:
    for k,v in tfidf.iteritems():
        for k1,v1 in v.iteritems():
            wf.write(k+'\t'+k1+'\t'+str(v1)+'\n')
