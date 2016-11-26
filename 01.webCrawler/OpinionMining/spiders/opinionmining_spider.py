#-------------------------------------------------------------------------------
# Name:        OpinionMiningSpider
# Purpose:     Use for my research -- Opinion Mining from Thai website
#              read start_urls from MySQL database
#              and use pipeline to insert item to MySQL database
# Author:      Phisan Sookkhee
# Created:     27 OCT 2016
# Edited:      23 NOV 2016
#-------------------------------------------------------------------------------
import scrapy
import pymysql
import csv
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from OpinionMining.items import OpinionminingItem
from urlparse import urlparse
from urlparse import urljoin

class OpinionMiningSpider(scrapy.Spider):
    name = "phisan"

    # Set start_urls from data in from CSV file
    # cr = csv.reader(open("/Users/phisan/Desktop/crawler/url.csv", "rb"))
    # start_urls = [line[2].strip() for line in cr]

    # Scrapy constructor
    # for receive command line argument
    # @param netloc is start domain for query link from database
    def __init__ (self, domain=None, netloc=None):
        self.netlocStart = netloc

    def parse(self, response):
        # Read allowed_domains from CSV file
        cr = csv.reader(open("/Users/phisanshukkhi/Desktop/crawler/allowed_domains.csv", "rb"))
        allowed_domains = [line[1].strip() for line in cr]

        selectors = [
            '//a',
        ]

        for selector in selectors:
            for sel in response.xpath(selector):
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

                        # Check link is in allowed domain
                        for allowed in allowed_domains:
                            if item['netloc'].find(allowed) >= 0 and item['netloc'] != "":
                                yield item
                                break

    # Set start_urls from data in database
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
        if self.netlocStart == None:
            self.cur.execute("SELECT link \
                              FROM spider \
                              ORDER BY id DESC")
        else:
            self.cur.execute("SELECT link \
                              FROM spider \
                              WHERE netloc LIKE %s \
                              ORDER BY id DESC", '%'+self.netlocStart+'%')
        rows = self.cur.fetchall()
        for row in rows:
            yield self.make_requests_from_url(row[0])

        self.conn.close()
