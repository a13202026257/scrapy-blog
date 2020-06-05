from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","cnblogs"])
# 启动某个爬虫的命令式：scrapy crawl 爬虫名称
# dirname指的是当前文件的父目录
# abspath指的是当前文件的目录