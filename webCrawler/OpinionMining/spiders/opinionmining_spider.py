import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from OpinionMining.items import OpinionminingItem
from urlparse import urlparse
from urlparse import urljoin

class OpinionMiningSpider(scrapy.Spider):
    name = "phisan"

    allowed_domains = ['*']
    start_urls = ['http://www.thairath.co.th/home',]

    def parse(self, response):
        for sel in response.xpath("//a"):
            item = OpinionminingItem()

            titles = sel.xpath('text()').extract()
            links = sel.xpath('@href').extract()

            # for multiple links
            if len(links) != 0:
                index = 0
                for link in links:
                    item['link'] = link
                    r = urlparse(link)
                    item['netloc'] = r[1]

                    if len(titles) != 0:
                        item['title'] = titles[index]
                    else:
                        item['title'] = titles

                    # for relative path link
                    if item['netloc'] == '':
                        item['link'] = urljoin(response.url, link)
                        r = urlparse(item['link'])
                        item['netloc'] = r[1]

                    index += 1
                    yield item
