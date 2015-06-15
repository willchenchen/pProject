#!/usr/bin/env python
# encoding: utf-8

import codecs
import numpy as np

def zip_f(pos,search_result):
    para=1.451385
    result=(1/pos**para)/sum(1/np.array(range(1,search_result+1))**para)
    return result

rf=codecs.open('/home/will/data/search_result_cn_phone.txt','r','utf-8')

appid=set()
rd=rf.readlines()
rf.close()
lrd=len(rd)

for x in rd:
    temp=x.split('\t')
    temp1=temp[1].split(',')
    for s in temp1:
        appid.add(s)

mtx=[]
for i,x in enumerate(rd):
    row=[]
    temp=x.split('\t')
    temp1=temp[1].split(',')
    for y in appid:
        if y in temp1:
            pos=temp1.index(y)+1
            nums=int(temp[2])
            row.append(zip_f(pos,nums))
        else:
            row.append(0)
    print i,x
    mtx.append(row)

mtx=np.array(mtx)
U,s,V=np.linalg.svd(mtx, full_matrices=False)
U=U[:,0:3]
s=s[0:3,0:3]
V=V[0:3,:]

result=[]
for i in range(lrd):
    row=[]
    for j in range(lrd):
        temp1=np.dot(U[i,:],U[j,:])
        temp2=np.linalg.norm(U[i,:])*np.linalg.norm(U[j,:])
        temp=temp1/temp2
        row.append(temp)
    result.append(row)

with codecs.open('/home/will/data/correlate.txt','w','utf8') as wf:
    for x in result:
        wf.write('\t'.join(str(s) for s in x)+'\n')

