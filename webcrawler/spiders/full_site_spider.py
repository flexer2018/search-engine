import sqlite3, traceback
from urllib.parse import urlparse
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
# from scrapy.linkextractors import LinkExtractor
from webcrawler.items import Page

class FullSiteSpider(Spider):
    name = 'full_site_spider'
    # custom_settings = {
    #     'ITEM_PIPELINES': {'FULL}
    # }

    def __init__(self, domain=None, *args, **kwargs):
        super(FullSiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://%s' % domain]
        self.recrawl_existing = False
        # self.con = sqlite3.connect('searchengine.db')
        # self.con.row_factory = sqlite3.Row
        # self.allowed_domains = [domain]

    def parse(self, response):
        # Could use CSS selectors here instead, e.g. https://github.com/scrapy/quotesbot/blob/master/quotesbot/spiders/toscrape-css.py
        # item = Page()
        # page['content'] = response.text
        # path = urlparse(response.url).path
        # print(traceback.print_stack())
        # try:
        #     sel = Selector(response)
        # except AttributeError:

        sel = Selector(response)
        page = Page()
        page['domain'] = urlparse(response.url).netloc
        page['url'] = response.url
        page['content'] = ''.join(sel.xpath("//body//text()").extract()).strip()
        yield page
        # cur = self.con.cursor()
        # print(response.url)
        # cur.execute("SELECT id FROM pages WHERE url=?", (response.url,))
        # res = cur.fetchone()
        # if res is None:
        #     cur.execute("INSERT INTO pages (url, path, content, last_crawled) VALUES (?, ?, ?, datetime('now'))", (response.url, urlparse(response.url).path, text_content))
        # elif self.recrawl_existing == True:
        #     cur.execute("UPDATE pages SET content=?, last_crawled=datetime('now') WHERE id=?", (text_content, res['id'] ))
        # self.con.commit()

        for link in response.css('a::attr(href)').extract():
            # Only follow links in this domain
            if urlparse(link).netloc != urlparse(response.url).netloc:
                continue
            # Don't recrawl existing pages if relevant setting is set
            # if self.recrawl_existing == False:
            #     cur.execute("SELECT id FROM pages WHERE url=?", (link,))
            #     res = cur.fetchone()
            #     if res is not None:
            #         continue
            yield response.follow(link, callback=self.parse)
            # yield scrapy.Request(link, callback=self.parse)

        # i = Item()
        # items = [i]
        # items = {'i': 33}
        # return items
        # return Request(link, callback=self.parse)

        # To recursively follow links I'll have to get all the links, as before, then 

        # return(page)
        # sel = Selector(response)
        # links = sel.xpath('//a')
        # items = []
        # for link in links:
        #     item = Page()
        #     item['link'] = link.xpath('@href').extract_first()
        #     items.append(item)

        # return(items)

