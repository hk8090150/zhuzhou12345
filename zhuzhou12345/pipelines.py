# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from logging import log

import pymysql
import json

from .settings import *



import scrapy
import json

class Zhuzhou12345Pipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        # 在初始化方法中打开文件
        self.fileName = open("Zhuzhou1.json", "wb")

    def process_item(self, item, spider):
        # 把数据转换为字典再转换成json
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写到文件中编码设置为utf-8
        self.fileName.write(text.encode("utf-8"))
        # 返回item
        return item

    def close_spider(self, spider):
        # 关闭时关闭文件
        self.fileName.close()

class DBPipeline():
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        # 通过cursor执行增量查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """insert into zhuzhou(Letter, LetterContent,LetterTime,LetterName,ReplyLetter,ReplyTime,Responders,url )
                                value (%s, %s, %s,%s, %s, %s, %s,%s)""",
                (item['Letter'],
                 item['LetterContent'],
                 item['LetterTime'],
                 item['LetterName'],
                 item['ReplyLetter'],
                 item['ReplyTime'],
                 item['Responders'],
                 item['url']))
            # item['publish_date'],
            # item['attachment_url'],
            # item['attachment_content']))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            pass
            # log(error)
        return item





