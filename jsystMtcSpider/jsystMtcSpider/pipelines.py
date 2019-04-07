# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from jsystMtcSpider.items import *

class JsystmtcspiderPipeline(object):

    def __init__(self):
        # 链接数据库
        self.conn = pymysql.connect(host='localhost', port=3306, user='test', passwd='123456', db='Tiku', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        '''
        处理item
        :param item: item 
        :param spider: item来自的爬虫
        :return:
        '''
        # 对item进行存储到数据库
        # ......
     
        if isinstance(item, JsystmtcspiderKmItem):
            sql2 = "insert into mtcTihao (km, question_num, area_code, question_type) values(%s, %s, %s, %s)"
            params2 = (str(item['km']),str(item['question_num']), str(item['area_code']), str(item['question_type']))
            self.cursor.execute(sql2, params2)
            self.conn.commit()
            return item
        
        elif isinstance(item,JsystmtcspiderKmQuestionItem):
            sql3 = "insert into mtcQuestion (km, question_num, question, img_url, answer, options, explanation) values(%s, %s, %s, %s, %s, %s, %s)"
            if(item['img_url']==None):
                item['img_url']='None'
            params3 = (str(item['km']),str(item['question_num']), str(item['question']), str(item['img_url']), str(item['answer']), str(item['options']) ,str(item['explanation']))
            self.cursor.execute(sql3, params3)
            self.conn.commit()
            return item #要记得最后将item给return出去，否则后续的pipeline将无法收到item进行处理

    def close_spider(self, spider):
        '''
        爬虫关闭后
        :param spider:
        :return:
        '''
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

