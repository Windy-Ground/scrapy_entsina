#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess

from sinaent.spiders.ent_spider import EntSpider


process = CrawlerProcess()
process.crawl(EntSpider)

process.start()
