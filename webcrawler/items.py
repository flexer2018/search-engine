# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Domain(Item):
    domain = Field()
    last_crawled = Field()

class Page(Item):
    domain = Field()
    domain_id = Field()
    url = Field()
    path = Field()
    content = Field()
    last_crawled = Field()