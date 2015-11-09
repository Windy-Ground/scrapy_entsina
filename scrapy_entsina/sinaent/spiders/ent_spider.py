#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import hashlib

from scrapy import Spider, Request

from sinaent.items import SinaentItem

def start_urls():
    """
    构造列表接口数据获取url
    :return:
    """
    # 最新菜单
    href_1 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=48&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_1_ = [href_1.format(_) for _ in range(1, 2886)]

    # 美图
    href_2 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=103&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_2_ = [href_2.format(_) for _ in range(1, 1150)]

    # 八卦
    href_3 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=49&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_3_ = [href_3.format(_) for _ in range(1, 1396)]

    # 电影
    href_4 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=50&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_4_ = [href_4.format(_) for _ in range(1, 888)]

    # 电视
    href_5 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=51&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_5_ = [href_5.format(_) for _ in range(1, 1346)]

    # 音乐
    href_6 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=52&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_6_ = [href_6.format(_) for _ in range(1, 954)]

    # 韩娱
    href_7 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=54&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_7_ = [href_7.format(_) for _ in range(1, 406)]

    # 视频
    href_8 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=123&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_8_ = [href_8.format(_) for _ in range(1, 127)]

    # 博客
    href_9 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=59&num=30&versionNumber=1.2.8&page={}&' \
             'encode=utf-8'
    href_9_ = [href_9.format(_) for _ in range(1, 119)]

    # 微博
    href_10 = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=2&lid=101&num=30&versionNumber=1.2.8&page={}&' \
              'encode=utf-8'
    href_10_ = [href_10.format(_) for _ in range(1, 369)]

    return href_1_ + href_2_ + href_3_ + href_4_ + href_5_ + href_6_ + href_7_ + href_8_ + href_9_ + href_10_


class EntSpider(Spider):
    name = 'ent_spider'
    start_urls = start_urls()

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,  # 设置请求延迟(默认请求过快，pycharm直接卡死)。即 相邻请求之间间隔的秒数
    }

    def parse(self, response):
        """
        对请求接口获取到的数据，进行处理
        :param response:
        :return:
        """
        result = json.loads(response.body)
        data = result.get('result').get('data') if result.get('result') else None
        if data:
            for item in data:
                yield Request(
                    item.get('url'),
                    callback=self.parse_details
                )

    def parse_details(self, response):
        """
        详细页信息获取
        :param response:
        :return:
        """
        item = SinaentItem()
        item['link'] = response.url
        item['text'] = self.hash_md5(response.url)
        item['title'] = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        item['desc'] = self.parse_desc(response)

        # 保存数据
        self.save_file(item['text'], item['title']+'\n'+item['desc'])

        yield item

    def hash_md5(self, text):
        hash_m5 = hashlib.md5()
        hash_m5.update(text)
        return hash_m5.hexdigest()

    def parse_desc(self, response):
        """
        初略获取文章内容
        :param response:
        :return:
        """
        desc = response.xpath('//div[@id="artibody"]//p[text()]/text()').extract()
        return '\n'.join([_.strip() for _ in desc if len(_) > 0])

    def save_file(self, f_name, f_desc):
        """
        将文件保存至data文件夹下
        :param f_name:
        :param f_desc:
        :return:
        """
        f_name = './data/' + f_name
        with open(f_name, 'w+') as f:
            f.write(f_desc)
