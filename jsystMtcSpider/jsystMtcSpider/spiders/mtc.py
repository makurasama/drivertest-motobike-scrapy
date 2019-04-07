# -*- coding: utf-8 -*-
import scrapy
import re
from jsystMtcSpider.items import *
import json

class MtcSpider(scrapy.Spider):
    name = 'mtc'
    allowed_domains = ['www.jsyst.cn/mtc']
    start_urls = ['http://www.jsyst.cn/mtc/']

    def parse(self, response):
        yield scrapy.Request('http://www.jsyst.cn/mtc/km1/fx' , callback=self.parse_question_mtc, dont_filter=True)
        yield scrapy.Request('http://www.jsyst.cn/mtc/km4/fx' , callback=self.parse_question_mtc, dont_filter=True)

    def parse_question_mtc(self, response):
        result = re.match(r'http://www.jsyst.cn/mtc/(\w+)/fx', response.url)
        print(result)
        km = result.group(1)  # 科目
        question_type = 'mtc'  # 类型

        question_detail = re.findall('(http://www.jsyst.cn/mtc/km[14]/fx/q(\d+)/)', response.text)
        for link, num in question_detail:
            kmItem = JsystmtcspiderKmItem(km=km, question_num=num, area_code='None', question_type=question_type)
            yield kmItem
            yield scrapy.Request(link, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):            
        result =  re.match('http://www.jsyst.cn/mtc/(\w+)/fx/q(\d+)', response.url, re.S)
        km = result.group(1) #科目
        question_num = result.group(2)  # 题号

        ele = response.xpath('//div[@class="vehiclesIn3"]')[0]
        question = ele.xpath('.//h1/text()').extract_first()
        img_url = ele.xpath('.//img/@src').extract_first()
        p = ele.xpath('//div[@class="vehiclesIn3"]/p')
        options = p[1: -3].xpath('./text()').extract()
        answer = p[-3].xpath('./font/b/text()').extract_first()
        explanation = p[-2].xpath('./text()').extract_first()
        questionItem = JsystmtcspiderKmQuestionItem(km=km,
                                                 question_num=question_num,
                                                 question=question,
                                                 img_url=img_url,
                                                 answer=answer,
                                                 options=json.dumps(options, ensure_ascii=False),
                                                 explanation=explanation)
        yield questionItem

        

    