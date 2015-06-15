#!/usr/bin/env python
# encoding: utf-8

import os
import codecs
import jieba

indir='/home/will/tmp/cmmt'
cmmt=[]

for x in os.listdir(indir):
    temp_file=codecs.open('/home/will/tmp/cmmt/%s'%x,'r','utf-16')
    for y in temp_file.readlines():
        temp=y.strip('\r\n').strip('<#####>').split('<#####>')
        try:
            if int(temp[4])<=3:
                temp_str=temp[1]+','+temp[5]
                cmmt.append(temp_str)
        except IndexError:
            pass
print len(cmmt)
cmmt1=[]
for x in cmmt:
    for y in jieba.cut(x,cut_all=False):
        if y not in cmmt1 and len(y)>1:
            cmmt1.append(y)
cmmt2=[]
for x in cmmt1:
    cnt=0
    for y in cmmt:
        if y.find(x)!=-1:
            cnt+=1
    cmmt2.append([x,str(cnt)])

write_file=codecs.open('/home/will/tmp/result.txt','w','utf-8')

for x in cmmt2:
    write_file.write('\t'.join(s for s in x)+'\r\n')

