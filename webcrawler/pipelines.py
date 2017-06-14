# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import sqlite3
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from webcrawler.items import Domain, Link
from webcrawler.spiders.mainspider import MainSpider

class WebcrawlerPipeline(object):

    def __init__(self):
        self.ds = None
        self.domain_id = None

    def open_spider(self, spider):
        # self.ds = dblite.open(Domain, 'sqlite://webcrawler.sqlite:domains', autocommit=True)
        # print(spider)
        # domain = Domain(domain=spider.allowed_domains[0])
        # print(domain)
        # self.ds.put(domain)
        # self.ds.commit()
        # self.ds.close()

        # self.ds = dblite.open(Link, 'sqlite://webcrawler.sqlite:links', autocommit=True)
        self.con = sqlite3.connect('webcrawler.sqlite')
        self.cur = self.con.cursor()
        self.cur.execute('insert into domains (domain) values (?)', [spider.allowed_domains[0]])
        res = self.cur.execute('select last_insert_rowid()')
        self.domain_id = res.fetchone()[0]
        print(333)
        print(dir())
        print(sys.path)
        print(999999)
        print(self.domain_id)
        self.con.commit()

    def close_spider(self, spider):
        self.con.commit()
        self.con.close()

    def process_item(self, item, spider):
        # print(111)
        # print(item)
        # if isinstance(item, Link):
        #     print(3333)
        #     try:
        #         self.ds.put(item)
        #     except dblite.DuplicateItem:
        #         raise DropItem("Duplicate item found: %s" % item)
        # else:
        #     raise DropItem("Unknown item type, %s" % type(item))
        self.cur.execute('insert into links (domain_id, link) values (?,?)', [self.domain_id, item['link']])
        return item
