# -*- coding: utf-8 -*-

from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaentPipeline(object):
    def process_item(self, item, spider):
        log.msg(item, log.INFO)
        return item
