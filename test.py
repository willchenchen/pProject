#!/usr/bin/env python
# encoding: utf-8

import codecs
import numpy as np

def zip_f(pos,search_result):
    para=1.451385
    result=(1/pos**para)/sum(1/np.array(range(1,search_result+1))**para)
    return result

print zip_f(1,155)
