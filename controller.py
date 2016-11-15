# -*- coding: utf-8 -*-

import pymysql
import os
import sys
import articleCrawler


class Connection:
    def __init__(self):
        """
            connect with mysql
        """
        self.db = pymysql.connect(
            user=os.getenv('MYSQL_USERNAME', ''),
            passwd=os.getenv('MYSQL_PASSWORD', ''),
            db=os.getenv('MYSQL_INSTANCE_NAME', ''),
            host=os.getenv('MYSQL_PORT_3306_TCP_ADDR', ''),
            port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306')),
            charset='utf8',
            use_unicode=False,
            init_command='SET NAMES UTF8'
        )
        cur = self.db.cursor()
        print("connection success!!")
        print(sys.stdin.encoding)

    def set_articles(self, specific_sector):
        """
            crawling article and save them to DB
        Args:
            specific_sector: list of crawling tags

        Returns:

        """
        a = articleCrawler.Crawler()

        sids = list()
        urls = dict()
        if specific_sector.__len__() == 0:
            sids = ["IT", "경제", "정치", "사회", "생활", "세계", "연예", "스포츠", "오피니언"]
        else:
            sids = specific_sector

        for sid in sids:
            urls = a.get_url(1, sid)


if __name__ == "__main__":
    c = Connection()
