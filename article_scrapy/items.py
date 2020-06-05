# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    #     这里可以做预处理 input_processor = MapCompose(加自己定义的处理函数)  这个库是在item.loader下面的 好像是
    #     也可以做个匿名函数lambda做简单处理
    url = scrapy.Field()
    front_image = scrapy.Field()
    front_image_path = scrapy.Field()
    author = scrapy.Field()
    front_num = scrapy.Field()
    pass


