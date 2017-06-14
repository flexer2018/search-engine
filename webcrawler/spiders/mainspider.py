from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from webcrawler.items import Link
# from scrapy.http import Request

class MainSpider(Spider):
    name = 'mainspider'
    # allowed_domains = ['willbeaufoy.net']
    # start_urls = ['http://willbeaufoy.net/']
    # allowed_domains = ['reddit.com']
    # start_urls = ['http://reddit.com/r/exmuslim']
    # allowed_domains = ['helenachance.com']
    # start_urls = ['http://helenachance.com']

    def __init__(self, domain=None, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://%s' % domain]

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//a')
        items = []
        for link in links:
            item = Link()
            item['link'] = link.xpath('@href').extract_first()
            items.append(item)

        return(items)

