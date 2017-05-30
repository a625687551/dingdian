# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # 小说名字:
    name = scrapy.Field()
    # 作者:
    author = scrapy.Field()
    # 小说地址:
    novelurl = scrapy.Field()
    # 小说状态:
    serialstatus = scrapy.Field()
    # 小说字数:
    serialnumber = scrapy.Field()
    # 小说类别:
    category = scrapy.Field()
    # 小说编号:
    name_id = scrapy.Field()


class DcontentItem(scrapy.Item):
    # 小说编号:
    id_name = scrapy.Field()
    # 章节内容:
    chaptercontent = scrapy.Field()
    # 绑定章节顺序:
    num = scrapy.Field()
    # 章节地址:
    chapterurl = scrapy.Field()
    # 章节名字:
    chaptername = scrapy.Field()
