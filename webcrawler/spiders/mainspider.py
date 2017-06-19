from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from webcrawler.items import Page

class MainSpider(Spider):
    name = 'mainspider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'webcrawler.pipelines.WebCrawlerPipeline': 500
        }
    }

    def __init__(self, domain=None, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://%s' % domain]

    def parse(self, response):
        # Could use CSS selectors here instead, e.g. https://github.com/scrapy/quotesbot/blob/master/quotesbot/spiders/toscrape-css.py
        sel = Selector(response)
        pages = sel.xpath('//a')
        items = []
        for page in pages:
            item = Page()
            item['link'] = link.xpath('@href').extract_first()
            items.append(item)

        return(items)

