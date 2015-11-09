#!/usr/bin/env python
# coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from scrapy.http import Request
from sinaent.items import textItem
from scrapy.contrib.spiders import Rule

import re


class TextSpider(Spider):
    name = "sinaenttext"  # name of spiders
    allowed_domains = ["ent.sina.com.cn"]
    # start_urls = ["http://ent.sina.com.cn/s/m/2015-10-09/doc-ifxirmqc4955025.shtml"]#http://ent.sina.com.cn
    start_urls = ["http://ent.sina.com.cn"]
    rules = [Rule(LinkExtractor(allow=[])), "parse_content"]

    def parse(self, response):  # rules得到的转移到这里，在Rule里面没有callback="parse",follow=True
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:
            if "//ent.sina.com.cn" in link.url:  # 如果是包含“//ent.sina.com.cn”的url，那么对其继续连接爬取分析
                yield Request(url=link.url, callback=self.parse_page)

    def parse_page(self, response):
        for link in LinkExtractor(allow=()).extract_links(response):
            if "//ent.sina.com.cn" in link.url:
                yield Request(url=link.url, callback=self.parse_page)
                yield Request(url=link.url, callback=self.parse_content)

    def parse_content(self, response):
        sel = Selector(response)
        url = response.url
        pattern = re.compile("(\w+)")
        write_name = pattern.findall(url)[-2]  # 将url倒数第二个数字字母作为文件名，

        texts = sel.xpath("//p/text()").extract()[:-5]  # 将<p></p>标签之间的文本提取出来，不包含“Corpright”等内容
        # write_text = open("texts3/" + write_name, "wb")
        # for i in texts:
        #     write_text.write(i)  # write to file
        # write_text.close()

        items = []
        item = textItem()
        for i in texts:
            if len(i) < 5:
                continue
            item["text"] = i
            items.append(item)
        return items
