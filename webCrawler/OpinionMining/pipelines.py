# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class OpinionminingPipeline(object):
    def __init__(self):
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

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO spider(title, netloc, link) \
                          VALUES (%s, %s, %s)", \
                          (item['title'], item['netloc'], item['link']))
        self.conn.commit()
        return item
