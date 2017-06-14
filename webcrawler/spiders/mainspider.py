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
    allowed_domains = ['helenachance.com']
    start_urls = ['http://helenachance.com']

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//a')
        items = []
        for link in links:
            item = Link()
            item['link'] = link.xpath('@href').extract_first()
            print(555)
            print(item['link'])
            items.append(item)

        return(items)

class MainCrawlSpider(CrawlSpider):
    name = 'maincrawlspider'
    # allowed_domains = ['willbeaufoy.net']
    # start_urls = ['http://willbeaufoy.net/']
    allowed_domains = ['helenachance.com']
    start_urls = ['http://helenachance.com']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = Selector(response)
        titles = hxs.xpath('//span[@class="pl"]')
        items = []
        for titles in titles:
            item = CraigslistSampleItem()
            item["title"] = titles.xpath("a/text()").extract()
            item["link"] = titles.xpath("a/@href").extract()
            items.append(item)
        return(items)

