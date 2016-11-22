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
import csv
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from OpinionMining.items import OpinionminingItem
from urlparse import urlparse
from urlparse import urljoin

class OpinionMiningSpider(scrapy.Spider):
    name = "phisan"

    start_urls = []

    # Read start_urls from CSV file
    cr = csv.reader(open("/Users/phisan/Desktop/crawler/url.csv", "rb"))
    start_urls = [line[2].strip() for line in cr]

    def parse(self, response):
        # Read allowed_domains from CSV file
        cr = csv.reader(open("/Users/phisan/Desktop/crawler/netloc.csv", "rb"))
        allowed_domains = [line[1].strip() for line in cr]

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

                    # Check link is in allowed domain
                    for allowed in allowed_domains:
                        if item['netloc'].find(allowed) > 0 and item['netloc'] != "":
                            yield item
                            break

    # def start_requests(self):
    #     self.conn = pymysql.connect(
    #         host='127.0.0.1',
    #         unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
    #         port=3306,
    #         user='web',
    #         passwd='web',
    #         db='opinion_spider',
    #         use_unicode=True,
    #         charset='utf8')
    #
    #     self.cur = self.conn.cursor()
    #
    #     # get data from database
    #     self.cur.execute("SELECT link FROM spider WHERE id>%s", 3000)
    #     rows = self.cur.fetchall()
    #     for row in rows:
    #         yield self.make_requests_from_url(row[0])
    #
    #     self.conn.close()
