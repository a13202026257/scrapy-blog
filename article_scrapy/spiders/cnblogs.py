# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request  # Request：将url请求传给scrapy的包
from urllib import parse  # 取出当前网页的域名
from scrapy.loader import ItemLoader
from test_scrapy.article_scrapy.items import ArticleItem


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/']

    # 函数部分
    def parse(self, response):
        # 获取整个页面的url,并交给scrapy下载并进行解析
        post_nodes = response.css("div.post_item ")
        for post_node in post_nodes:
            # response.url + post_url   #如果网页中只有相关的编号，那么就要主域名+post_url
            # Request(url=parse.urljoin(response.url,post_url), callback=self.parse_selector)  #urljoin可以得出 主域名+子目录=当前的网页
            image_url = post_node.css("div.post_item_body p a img::attr(src)").extract_first("")
            recom_num = post_node.css("div.diggit span::text").extract_first("")
            if image_url:
                image_url = 'https:' + image_url
            post_url = post_node.css("div.post_item_body h3 a::attr(href)").extract_first("")
            yield Request(url=post_url, meta={"front_img":image_url,"front_recom":recom_num}, callback=self.parse_selector)  # yield自动交给scrapy去下载
            print(post_url)

        # 提取下一页的URL，并交给scrapy下载并进行解析
        next_url = response.xpath("//*[@class='pager']/a[last()]/@href").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url,post_url), callback=self.parse)

    # 选择器部分
    def parse_selector(self, response):
        article_item = ArticleItem()  # 实例化一个Item
        front_image = response.meta.get("front_img", "")  # get方法不会抛异常，赋给默认值为空
        title = response.xpath("//*[@id='cb_post_title_url']/text()").extract_first("")
        author_re = response.css("title::text").extract_first("")
        author = re.match(".*?(-\s.+\s-).*",author_re)
        if author:
            author = author.group(1).replace("-","").replace(" ","")
        front_num = response.meta.get("front_recom","")
        pass
        # comment_count = response.css("#stats-comment_count::text").extract()[0]  #收藏数
        # view_count = response.css ("span#post_view_count::text").extract_first("")

        # ast = re.match(".*?(\d+).*", comment_count)
        # if ast:
        #     comment_count = int(ast.group(1))
        # else:
        #     comment_count = 0

        # text仅仅返回所指元素的文本内容
        # 要从源HTML文件中找
        pass
        # 给item传值
        article_item["title"] = title
        article_item["front_image"] = [front_image]  # settings中传入的是一个数组，假如这里是值的话会报错
        article_item["url"] = response.url
        article_item["author"] = author
        article_item["front_num"] = [front_num]

        yield article_item
        pass
#     title =response.xpath("//a[contains(@class,'postTitle2')]/text()").extract()
#     调用xpath的contains函数，匹配到包含class的标识符


# 知识点2  ：
#    过滤表达式：a for a in list if not a.strip().endwith('')
# 知识点3  :
# CSS选择器：
# title = response.css(".entry-header h1::text").extract()[0] :[0]指只取第一个数
# 知识点3  ：
# extract().strip()函数，去掉空格，默认以空格分隔

# 知识点4：
# CSS选择器(".可以是class中的一个属性，但要全局唯一")

# 知识点5：
 #通过item loader加载item
        # front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        # item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader.add_css("title", ".entry-header h1::text")
        # item_loader.add_value("url", response.url)
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        # item_loader.add_value("front_image_url", [front_image_url])
        # item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        # item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        # item_loader.add_css("fav_nums", ".bookmark-btn::text")
        # item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        # item_loader.add_css("content", "div.entry")
        #
        # article_item = item_loader.load_item()
#         item_loader让代码更整洁外，还能动态的更新抓取的规则，比如规则可以从数据库中读取！再配置映射，然而还没学到
# 就用旧的吧

# 知识点6：
#             正则里出现双引号，两边用''


