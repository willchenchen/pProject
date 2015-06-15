#!/usr/bin/env python
# encoding: utf-8

from elasticsearch import Elasticsearch
import types,json,sys

es = Elasticsearch("115.159.25.211:9200")

query = {'query':{'filtered':{'query':{}}}}

def searchWord(words,appids,sdate,edate,size):
    boolQry = {'bool':{'should':[],'must':[],'minimum_should_match':1}}

    if words and type(words) is types.ListType:
        for w in words:
            boolQry['bool']['should'].append({'term':{'word':w}})
    elif words and type(words) is not types.ListType:
        boolQry['bool']['must'].append({'term':{'word':words}})

    if appids and type(appids) is not types.ListType:
        boolQry['bool']['must'].append({'term':{'appid':appids}})
    elif appids and type(appids) is types.ListType:
        fbool = {'bool':{'should':[]}}
        for id in appids:
            fbool['bool']['should'].append({'term':{'appid':id}})
        query['query']['filtered']['filter'] = fbool

    boolQry['bool']['must'].append({'range':{'date':{'gte':sdate,'lte':edate}}})

    query['sort'] = {'rank':{'order':'asc'}}
    if words and appids and type(appids) is types.ListType and type(words) is types.ListType:
        query['size'] = len(words) * len(appids) * size
    elif words and appids and type(appids) is types.ListType:
        query['size'] = len(appids) * size
    elif words and appids and type(words) is types.ListType:
        query['size'] = len(words) * size
    elif words and type(words) is types.ListType and appids is None:
        query['size'] = len(words) * size
    elif appids and type(appids) is types.ListType and words is None:
        query['size'] = len(appids) * size
    else:
        query['size'] = size

    query['query']['filtered']['query'] = boolQry

    print query
    #print json.dumps(query, encoding = 'utf-8', ensure_ascii = False)
    print es.search(index = 'apple_search_result_cn_phone', body=query)
