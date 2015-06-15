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

'''
appid={}
file2=codecs.open('/home/will/tmp/app_cate.txt','r','utf8')
for x in file2:
    temp=x.strip('\r\n').replace(u'\ufeff','').split('\t')
    if temp[1].find('6012')!=-1 and temp[0] not in appid:
        appid[temp[0]]=[]
'''

appid={}
file2=codecs.open('/home/will/tmp/wa_test.txt','r','utf8')
for x in file2:
    temp=x.strip('\r\n').split('\t')
    appid[temp[0]]=temp[3]

i=0
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
        i+=1
    if i%10000==0:
        print i

if len(appid)!=len(app_fenci):
    print len(appid),len(app_fenci)

ci={}
for x in app_fenci.itervalues():
    for y in x:
        if y not in ci:
            ci[y]=[]

tf1=0
tf2=0
df=0
ndoc=len(app_fenci)
for x in ci.keys():
    for j,y in app_fenci.iteritems():
        wc=collections.Counter(y)
        if wc.get(x)!=None:
            df+=1
            tf1+=float(wc.get(x))**2
            tf2+=float(wc.get(x))
    #if df==1:
    #    del ci[x]
    #else:
    tf3=tf1-float(1/ndoc)*tf2**2
    ci[x].extend([df,tf3])
    tf1=0
    tf2=0
    df=0

length=int(len(ci)*0.15)
order_ci=sorted(ci.items(),key=lambda t:t[1][1],reverse=True)[:length]

id_ci=[]
temp=[]
for i,x in app_fenci.iteritems():
    for y in order_ci:
        wc=collections.Counter(x)
        if wc.get(y[0])!=None:
            tfidf=float(wc.get(y[0]))*math.log(ndoc/float(y[1][0]))
        else:
            tfidf=0
        temp.append(tfidf)
    id_ci.append(temp)
    temp=[]

id_ci=np.array(id_ci)
id_ci=scale(id_ci)
id_target=np.array([appid.get(x) for x in app_fenci])

print id_ci
print id_target

#pca = PCA(n_components=5).fit(id_ci)
reduced_data = PCA(n_components=5).fit_transform(id_ci)
estimator=KMeans(init='k-means++', n_clusters=5, n_init=10)
estimator.fit(reduced_data)

write_file=codecs.open('/home/will/tmp/temp.txt','w','utf8')
i=0
for x in app_fenci:
    write_file.write(str(x)+'\t'+str(appid.get(x))+'\t'+str(estimator.labels_[i])+'\r\n')
    i+=1

print metrics.homogeneity_score(id_target, estimator.labels_)
print metrics.completeness_score(id_target, estimator.labels_)
print metrics.v_measure_score(id_target, estimator.labels_)
print metrics.adjusted_rand_score(id_target, estimator.labels_)
print metrics.adjusted_mutual_info_score(id_target,  estimator.labels_)
print metrics.silhouette_score(id_ci, estimator.labels_,metric='euclidean')

