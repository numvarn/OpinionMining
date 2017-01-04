#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql

class GetPath:
    """docstring for GetPathh"""
    def __init__(self, netloc):
        self.cur = ''
        self.netloc = netloc
        self.connect()

    def connect(self):
        conn = pymysql.connect(
            host='127.0.0.1',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            port=3306,
            user='web',
            passwd='web',
            db='opinion_spider',
            use_unicode=True,
            charset='utf8')

        self.cur = conn.cursor()

        # Get all from Database
        self.cur.execute("SELECT * FROM spider WHERE netloc LIKE %s ORDER BY id ASC", ('%'+self.netloc+'%'))
        self.cur.close()
        conn.close()

    def getResult(self):
        return self.cur.fetchall()


if __name__ == '__main__':
    getPath = GetPath(1, 20)
    rows = getPath.getResult()
    for row in rows:
        print row[0]," : ",row[1].encode('utf-8', 'replace'), " : ", row[2]
