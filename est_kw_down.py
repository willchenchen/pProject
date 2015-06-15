#!/usr/bin/env python
# encoding: utf-8

import codecs
import numpy as np
import MySQLdb

def zip_f(pos,search_result):
    para=1.451385
    result=(1/pos**para)/sum(1/np.array(range(1,search_result+1))**para)
    return result

rf=codecs.open('/Users/will/myData/search_result_cn.txt','r','utf-8')
rf1=codecs.open('/Users/will/myData/search_result_cn_phone.txt','r','utf-8')

host='123.57.66.5'
user='will'
passwd='qweasd123'
db='asou_data'
port=3306

ctd=MySQLdb.Connect(host,user,passwd,db,port,charset='utf8')
cur=ctd.cursor()

popList=[27,30]
genreList=[36,6014,7010,6017,6021,6008,6007,6012,6013,6003,6011,6004,6000,6009,6002,6016,6005,6023,6015,6006,6010,6020,6018,6001,6022]
gameList=[6014,7016,7001,7006,7009,7018,7005,7002,7008,7019,7012,7004,7015,7017,7003,7014,7013,7011,7007]
magList=[6021,13017,13010,13018,13009,13030,13015,13024,13003,13004,13013,13019,13008,13001,13029,13006,13002,13012,13021,13011,13020,13027,13025,13007,13005,13028]

popId=','.join(str(s) for s in popList)
genreId=','.join(str(s) for s in genreList)+','+','.join(str(m) for m in gameList)+','+','.join(str(n) for n in magList)

sql="select distinct popId,genreId,appids from list_rank_cn_table where date='2015-03-26' and genreId in (%s) and popId in (%s)"
cur.execute(sql%(genreId,popId))

tempData={}
for x in cur.fetchall():
    if x[1]==36 and x[0]==27:
        tempLen=len(x[2].split(','))
        totalHits27=0.7/zip_f(1,tempLen)/zip_f(1,25)
    if x[1]==36 and x[0]==30:
        tempLen=len(x[2].split(','))
        totalHits30=0.7/zip_f(1,tempLen)/zip_f(1,25)
    
    if str(x[0])+'|'+str(x[1]) not in tempData:
        tempData[str(x[0])+'|'+str(x[1])]=x[2]
    else:
        print "榜单数据不唯一"
ctd.close()

appPect={}
for x in popList:
    for i,y in enumerate(genreList):
        if y not in (6014,6021):
            temp=str(x)+'|'+str(y)
            if tempData.get(temp)!=None:
                temp1=tempData.get(temp).split(',')
                temp2=len(temp1)
                for j,z in enumerate(temp1):
                    if z not in appPect:
                        appPect[z]=eval('totalHits%s'%x)*zip_f(i+1,25)*zip_f(j+1,temp2)
                    else:
                        appPect[z]=appPect[z]+eval('totalHits%s'%x)*zip_f(i+1,25)*zip_f(j+1,temp2)
        elif y==6014:
            for j,z in enumerate(gameList):
                temp=str(x)+'|'+str(z)
                if tempData.get(temp)!=None:
                    temp1=tempData.get(temp).split(',')
                    temp2=len(temp1)
                    for k,r in enumerate(temp1):
                        if r not in appPect:
                            appPect[r]=eval('totalHits%s'%x)*zip_f(2,25)*zip_f(j+1,19)*zip_f(k+1,temp2)
                        else:
                            appPect[r]=appPect[r]+eval('totalHits%s'%x)*zip_f(2,25)*zip_f(j+1,19)*zip_f(k+1,temp2)
        else:
            for j,z in enumerate(magList):
                temp=str(x)+'|'+str(z)
                if tempData.get(temp)!=None:
                    temp1=tempData.get(temp).split(',')
                    temp2=len(temp1)
                    for k,r in enumerate(temp1):
                        if r not in appPect:
                            appPect[r]=eval('totalHits%s'%x)*zip_f(5,25)*zip_f(j+1,26)*zip_f(k+1,temp2)
                        else:
                            appPect[r]=appPect[r]+eval('totalHits%s'%x)*zip_f(5,25)*zip_f(j+1,26)*zip_f(k+1,temp2)

print max(appPect.values())

app_down=[]
for x in rf:
    try:
        temp=x.strip('\r\n').split('\t')
        if appPect.get(temp[0])!=None:
            print "有值"
            app_down.append([temp[0],round(int(temp[3])*(1-appPect.get(temp[0])),3)])
        else:
            app_down.append([temp[0],round(int(temp[3]),3)])
    except IndexError:
        print '##############'
        print x
        print len(x.strip('\r\n').split('\t'))
        print '##############'
        pass
rf.close()

app_kw={}
for x in rf1:
    try:
        temp=x.strip('\n').split('\t')
        temp1=temp[1].split(',')
        for i,y in enumerate(temp1):
            temp2=round(zip_f(i+1,int(temp[2]))*int(temp[3]),2)
            if y not in app_kw:
                app_kw[y]={temp[0]:temp2}
            else:
                app_kw[y][temp[0]]=temp2
    except (IndexError,ValueError) as e:
        print '##############'
        print x
        print len(x.strip('\r\n').split('\t'))
        print '##############'
        pass
rf1.close()

result={}
for x in app_down:
    temp=app_kw.get(x[0])
    if temp:
        temp1=sum(temp.values())
        for key,value in temp.iteritems():
            try:
                result[key+'|'+x[0]]=float(value)/temp1*int(x[1])
            except ZeroDivisionError:
                print temp
                pass

with codecs.open('/Users/will/myData/fenciDown.txt','w','utf-8') as wf:
    for k,v in result.iteritems():
        temp=k.split('|')
        wf.write(temp[0]+'\t'+temp[1]+'\t'+str(v)+'\n')

