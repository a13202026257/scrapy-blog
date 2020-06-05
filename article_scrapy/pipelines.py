# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs  # 避免很多编码方面的繁杂工具 ，也是打开
import json  # 一种文件格式
import MySQLdb   #导入数据库的库
from scrapy.exporters import JsonItemExporter

class TestScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

# 自定义Json文件导入
class JsonPipeline(object):
    def __init__(self):  # 初始化实例self的值
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"  # ensure很重要，ture时直接将中文变成unicode，json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
        self.file.write(lines)
        return item  # 返回item，给下一个管道用

    def spider_closed(self, spider):  # 当spider关闭的时候，这里的函数就会被调用
        self.file.close()

# 定义数据库
class MysqlPipeline(object):
    def __init__(self):
        self.conn =MySQLdb.connect(host='localhost',user='root',passwd='root',db='spider',port=3306,charset="utf8",use_unicode =True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = ("\n"
                      "            insert into cnblogs_info(title,author,recom,url,front_image)\n"
                      "            VALUES (%s, %s, %s, %s, %s)\n")

        self.cursor.execute(insert_sql, (item["title"], item["author"], item["front_num"], item["url"], item["front_image"]))
        self.conn.commit()
        pass


class ArticleImagePipeline(ImagesPipeline):    #定义自己的imagespipeline，那首先要继承原生的imagespipeline
    def item_completed(self, results, item, info):
        if "front_image" in item:
            for ok, value in results:        #value是键值对，results也是
                image_file_path = value["path"]   #取path的值
            item["front_image_path"] = image_file_path
        return item


# 下面的功能和自定义json导出一样

# class JsonExporterPipleline(object):
#     #调用scrapy提供的json export导出json文件
#     def __init__(self):
#         self.file = open('articleexport.json', 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
