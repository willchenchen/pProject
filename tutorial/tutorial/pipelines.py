# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class TutorialPipeline(object):
#    def process_item(self, item, spider):
#        return item

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            req=scrapy.Request(image_url,
                    cookies={'CNZZDATA1188895':'cnzz_eid%3D211341207-1414037741-http%253A%252F%252Fwww.tigtag.com%252F%26ntime%3D1414592071',' __utma':'249898069.1538312212.1414037748.1414587889.1414592072.22',' __utmz':'249898069.1414592072.22.10.utmcsr',' CNZZDATA4107239':'cnzz_eid%3D1666246005-1414037883-http%253A%252F%252Fbbs.tigtag.com%252F%26ntime%3D1414592071',' uchome_loginuser':'willchenchen',' 9Mjd_2132_saltkey':'SXObb30c',' 9Mjd_2132_lastvisit':'1414508907',' 9Mjd_2132_sid':'Aa617R',' 9Mjd_2132_lastact':'1414592215%09misc.php%09secqaa',' 9Mjd_2132_visitedfid':'48D182',' 9Mjd_2132_forum_lastvisit':'D_182_1414569311D_48_1414592200',' 9Mjd_2132_ulastactivity':'1b6fGMQWxTRiMSzp420WgrKoRu88WZstFmDJHCR0cOWmY4gYgtBV',' 9Mjd_2132_auth':'bed5VlbVamD5wvi%2BzH2q8q9InV8O%2Fc%2FSafI7N70l4Js94pEPOK53R1Nzk%2FF3S0c59XElffA5X5wuNo%2Fb5d3MZ2h%2Bpt8',' 9Mjd_2132_lastcheckfeed':'370250%7C1414565985',' 9Mjd_2132_security_cookiereport':'4f9342DnFLoVpuf038KFd3%2F2TaSr3rqgsC1LaLdeibM%2BPYXbeoQv',' 9Mjd_2132_connect_is_bind':'0',' 9Mjd_2132_smile':'2D1',' 9Mjd_2132_nofavfid':'1',' tigtag_auth':'b3ffbz3nv3J8D4dfBKTUn%2BRggp0eEsQYFGcD%2FJxh3za2IU%2BIqcjtt47Z4HWrStDN',' poK_authid':'370250',' __jsluid':'575b240484fbf115aef121d98557096c',' 9Mjd_2132_lip':'106.187.36.4%2C1414592202',' 9Mjd_2132_sendmail':'1',' 9Mjd_2132_checkpm':'1',' __utmb':'249898069.6.10.1414592072',' __utmc':'249898069',' __utmt':'1',' 9Mjd_2132_secqaaSyYxga20':'7062FDD8RPKUIxsRNCMQVtBaiw70J7nRBhRHXtkRO7dlIZl2LghJBsOQegTumgHYvy88az61vjQKf4RfQLBsaKOMC0eYgGcOOBvV8SMb%2FCT9rPymr0VPmewQ',' 9Mjd_2132_viewid':'tid_3425573',' 9Mjd_2132_secqaaSAa617R0':'75dfgOix2LNV0rWZixgjJrh0MW80zYCEz5JIn1dZIDpM3Wmf7s1yWTyRBTGif3aax%2BDrRspkORHEtvpT73cd3h%2FaoEmozVub4%2FQ8TkZFyKzDoiPlDtOx512o'})
            req.meta['proxy']="http://127.0.0.1:8118"
            yield req

    #def item_completed(self, results, item, info):
    #    image_paths = [x['path'] for ok, x in results if ok]
    #    if not image_paths:
    #        raise DropItem("Item contains no images")
    #    item['image_paths'] = image_paths
    #    return item

