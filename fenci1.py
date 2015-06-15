#!/usr/bin/env python
# encoding: utf-8

import codecs
import re
import jieba.posseg as pseg
import collections
import math
import numpy as np

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA

def txt_cluser(app_fenci_temp):
    ci={}
    for x in app_fenci_temp.itervalues():
        for y in x:
            if y not in ci:
                ci[y]=[]
    tf1=0
    tf2=0
    df=0
    ndoc=len(app_fenci_temp)
    for x in ci.keys():
        for j,y in app_fenci_temp.iteritems():
            wc=collections.Counter(y)
            if wc.get(x)!=None:
                df+=1
                tf1+=float(wc.get(x))**2
                tf2+=float(wc.get(x))
        tf3=tf1-float(1/ndoc)*tf2**2
        ci[x].extend([df,tf3])
        tf1=0
        tf2=0
        df=0

    length=int(len(ci)*0.15)
    order_ci=sorted(ci.items(),key=lambda t:t[1][1],reverse=True)[:length]

    id_ci=[]
    temp=[]
    id_temp=[]
    for i,x in app_fenci_temp.iteritems():
        for y in order_ci:
            wc=collections.Counter(x)
            if wc.get(y[0])!=None:
                tfidf=float(wc.get(y[0]))*math.log(ndoc/float(y[1][0]))
            else:
                tfidf=0
            temp.append(tfidf)
        id_ci.append(temp)
        temp=[]
        id_temp.append(i)

    id_ci=np.array(id_ci)
    id_ci=scale(id_ci)

    reduced_data = PCA(n_components=5).fit_transform(id_ci)
    estimator=KMeans(init='k-means++', n_clusters=5, n_init=10)
    estimator.fit(reduced_data)

    result={}
    for i,x in enumerate(id_temp):
        result[x]=estimator.labels_[i]
    return result


appid={}
file2=codecs.open('/home/will/tmp/wa_test.txt','r','utf8')
for x in file2:
    temp=x.strip('\r\n').split('\t')
    appid[temp[0]]=temp[3]

file1=codecs.open('/home/will/tmp/app_info_description_cn.txt','r','utf8')
app_fenci={}
temp=''
while True:
    tempread=file1.read(8192)
    tempread=temp+tempread
    if not tempread:break
    tempread=tempread.replace(u'\ufeff','').replace(u'\u2028','').replace('\n','')
    tempread=tempread.split('@@@|||@@@\r')
    temp=tempread.pop()
    for x in tempread:
        t1=x.split('\t@@@|||@@@')
        if re.search(ur'[\u4e00-\u9fa5]+',t1[1])!=None and t1[0] in appid:
            fc_temp=[s.word for s in pseg.cut(t1[1].strip('\r\n')) if s.flag=='n' and len(s.word)>1]
            app_fenci[t1[0]]=fc_temp

result=txt_cluser(app_fenci)
wc=collections.Counter(result.values())
print wc
while max(wc.values())>10:
    for i,x in wc.iteritems():
        if x>10:
            app_fenci_temp={}
            for j,y in result.iteritems():
                if y==i:
                    app_fenci_temp[j]=app_fenci.get(j)
            result_temp=txt_cluser(app_fenci_temp)
            print i,x,collections.Counter(result_temp.values())
            a=max(result.values())+1
            for k,z in result_temp.iteritems():
                if (z+i)!=i:
                    result[k]=a
    wc=collections.Counter(result.values())
    print wc

t1=[]
t2=[]

write_file=codecs.open('/home/will/tmp/temp.txt','w','utf8')
for i,x in result.iteritems():
    t1.append(x)
    t2.append(appid.get(i))
    write_file.write(str(i)+'\t'+str(x)+'\t'+str(appid.get(i))+'\r\n')

print len(set(t1))
print len(set(t2))
print metrics.homogeneity_score(t1,t2)
print metrics.completeness_score(t1,t2)
print metrics.v_measure_score(t1, t2)
print metrics.adjusted_rand_score(t1,t2)
print metrics.adjusted_mutual_info_score(t1,t2)


