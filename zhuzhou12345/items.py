# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Zhuzhou12345Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Letter = Field()  # 信件标题
    LetterContent = Field()  # 来信内容
    LetterTime = Field()  # 来信时间
    LetterName = Field()  # 来信人名字
    ReplyLetter = Field()  # 来信答复
    ReplyTime = Field()  # 回信时间
    Responders = Field()   # 回信者单位或名字
    url = Field()    # 详细url连接网址
    Page_ClickCount = Field()  # 点击次数





