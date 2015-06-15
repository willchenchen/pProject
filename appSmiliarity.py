#!/usr/bin/env python
# encoding: utf-8

import codecs
import numpy as np

def zip_f(pos,search_result):
    para=1.451385
    result=(1/pos**para)/sum(1/np.array(range(1,search_result+1))**para)
    return result

rf=codecs.open('/home/willchen/data/search_result_cn_phone.txt','r','utf-8')

app_kw={}
i=0
for x in rf:
    tmp=x.split('\t')
    for i,y in enumerate(tmp[1].split(',')):
        try:
            if y not in app_kw:
                app_kw[y]={tmp[0]:zip_f(float(i+1),int(tmp[2]))}
            else:
                app_kw[y][tmp[0]]=zip_f(float(i+1),int(tmp[2]))
        except (IndexError,ValueError) as e:
            print '##############'
            print x
            print len(x.strip('\r\n').split('\t'))
            print '##############'
            pass
	i+=1
    if i%5==0:
	break


result={}
keyset=set()
for k,v in app_kw.iteritems():
    keyset.add(k)
    for k1,v1 in app_kw.iteritems():
        if k1 not in keyset:
            inter_tmp=set(v.keys()).intersection(v1.keys())
            inter_len=len(inter_tmp)
            inter_tol=set(v.keys()+v1.keys())
            if inter_len!=0:
                dism=0
                for x in inter_tmp:
                    dism+=abs(v.get(x)-v1.get(x))
                result[k+'|'+k1]=1/dism*inter_len*inter_len
rf.close()

with codecs.open('/home/willchen/data/appSimilirity.txt','w','utf-8') as wf:
    for k,v in result.iteritems():
        tmp=k.split('|')
        wf.write(tmp[0]+'\t'+tmp[1]+'\t'+str(v)+'\n')
