#-------------------------------------------------------------------------------
# Name:        OpinionMiningSpider
# Purpose:     Use for my research -- Opinion Mining from Thai website
#              read start_urls from MySQL database
#              and use pipeline to insert item to MySQL database
# Author:      Phisan Sookkhee
# Created:     27 OCT 2016
#-------------------------------------------------------------------------------
import scrapy
import pymysql
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from OpinionMining.items import OpinionminingItem
from urlparse import urlparse
from urlparse import urljoin

class OpinionMiningSpider(scrapy.Spider):
    name = "phisan"

    allowed_domains = ['*']
    start_urls = ['http://www.thairath.co.th/home',]
    # start_urls = []

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

    def start_requests(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            port=3306,
            user='web',
            passwd='web',
            db='opinion_spider',
            use_unicode=True,
            charset='utf8')

        self.cur = self.conn.cursor()

        # get data from database
        self.cur.execute("SELECT link FROM spider WHERE id>%s", 1)
        rows = self.cur.fetchall()
        for row in rows:
            yield self.make_requests_from_url(row[0])

        self.conn.close()
