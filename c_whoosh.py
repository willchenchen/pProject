#!/usr/bin/env python
# encoding: utf-8

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT,ID
import os
import codecs

dir_index='/home/will/tmp/search_index'

if not os.path.exists(dir_index):
    os.mkdir(dir_index)
schema=Schema(cmt_id=ID(stored=True),content=TEXT(stored=True))
ix=create_in(dir_index,schema)
writer=ix.writer(multisegment=True)

file1=codecs.open('/home/will/tmp/cmmt/cn_385285922_current.txt','r','utf-16')
for x in file1.readlines():
    temp=x.strip('\r\n').strip('<#####>').split('<#####>')
    try:
        if int(temp[4])<4:
            string=temp[1]+','+temp[5]
            writer.add_document(cmt_id=u'%s'%temp[0],content=u'%s'%string)
    except IndexError:
        pass
writer.commit()


