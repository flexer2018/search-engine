# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import sqlite3
from datetime import datetime
from urllib.parse import urlparse
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from webcrawler.items import Domain, Link
from webcrawler.spiders.mainspider import MainSpider

class WebcrawlerPipeline(object):

    def __init__(self):
        self.domain_id = None

    def open_spider(self, spider):
        self.con = sqlite3.connect('searchengine.db')
        self.cur = self.con.cursor()
        domain = urlparse(spider.start_urls[0]).netloc
        self.cur.execute("SELECT * FROM domains WHERE domain =?", [domain])
        res = self.cur.fetchone()
        if res is None:
            self.cur.execute("INSERT INTO domains (domain, last_crawled) VALUES (?, datetime('now'))", [domain])
            self.cur.execute('SELECT last_insert_rowid()')
            self.domain_id = self.cur.fetchone()[0]
        else:
            self.domain_id = res[0]
            self.cur.execute("UPDATE domains SET last_crawled=datetime('now') WHERE id=?", [self.domain_id])
        self.con.commit()

    def close_spider(self, spider):
        self.con.commit()
        self.con.close()

    def process_item(self, item, spider):
        # If link is for a newly encountered domain, add it to the domains table
        parsed_url = urlparse(item['link'])
        if parsed_url.netloc != '':
            self.cur.execute("SELECT * FROM domains WHERE domain =?", [parsed_url.netloc])
            res = self.cur.fetchone()
            if res is None:
                self.cur.execute("INSERT INTO domains (domain) VALUES (?)", [parsed_url.netloc])

        # If link doesn't yet exist in links table, add it
        self.cur.execute("SELECT * FROM links WHERE link =?", [item['link']])
        res = self.cur.fetchone()
        if res is None:
            self.cur.execute("INSERT INTO links (domain_id, link) VALUES (?,?)", [self.domain_id, item['link']])

        return item
