# -*- coding: utf-8 -*-

import pymysql
import os
import sys
import re
from articleCrawler import Crawler
from articleDTO import Article
from splitArticle import Splitting


class Controller:
    def __init__(self, name, password, db, host):
        """
        Connect to mysql
        """
        self.db = pymysql.connect(
            user=os.getenv('MYSQL_USERNAME', name),
            passwd=os.getenv('MYSQL_PASSWORD', password),
            db=os.getenv('MYSQL_INSTANCE_NAME', db),
            host=os.getenv('MYSQL_PORT_3306_TCP_ADDR', host),
            port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306')),
            charset='utf8',
            use_unicode=False,
            init_command='SET NAMES UTF8'
        )
        check_connection = self.db.cursor()
        print("connection success!!")
        print(sys.stdin.encoding)

    def article_process(self, specific_sector):
        """
        Crawling articles and save them to DB

        Args:
            specific_sector: list of crawling tags
        """
        cr = Crawler()

        sids = list()
        urls = list()
        contents = list()
        if specific_sector.__len__() == 0:
            sids = ["IT", "경제", "정치", "사회", "생활", "세계", "연예", "스포츠", "오피니언"]
        else:
            sids = specific_sector

        for sid in sids:
            urls = cr.get_url(1, sid)
            urls = cr.get_news(urls)
            contents = cr.get_content(urls, sid)
            self.set_articles(contents)

    def set_articles(self, contents):
        """
        Send query for article insertion

        Args:
            contents: list of article contents
        """
        cur = self.db.cursor()
        sql = ""
        for info in contents:
            sql = "INSERT INTO article (title, acontents, tag, subtag, scheck, wcheck) "\
                      "SELECT %s, %s, %s, %s, 0, 0 FROM DUAL "\
                      "WHERE NOT EXISTS (SELECT title FROM article WHERE title=%s)"
            values = (info.get_title, info.get_content, info.get_tag, info.get_sub_tag, info.get_title)
            cur.execute(sql, values)
            self.db.commit()
            print("Article Insertion Success!\n[%s]" % str(info))

    def get_ariticles(self, tag, mode):
        """
        Get articles from DB according to mode and tag

        Args:
            tag: wanted tag for searching
            mode: sentence or word

        Returns: list of article DTOs
        """
        cur = self.db.cursor()
        sql = ""
        contents = list()

        if mode == "s":
            sql = """SELECT * FROM article WHERE tag=%s AND scheck=0"""
        elif mode == "w":
            sql = """SELECT * FROM article WHERE tag=%s AND wcheck=0"""
        else:
            print("Mode error")
            return contents

        values = (tag)
        cur.execute(sql, values)
        # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        if total < 1:
            print('No Articles')
        else:
            for record in range(total):
                content = Article()
                content.set_id(row[record][0])
                content.set_title(row[record][1].decode('utf8', 'surrogatepass'))
                content.set_content(row[record][2].decode('utf8', 'surrogatepass'))
                content.set_tag(row[record][3].decode('utf8', 'surrogatepass'))
                content.set_sub_tag(row[record][4].decode('utf8', 'surrogatepass'))
                content.set_scheck(row[record][5])
                content.set_wcheck(row[record][6])
                contents.append(content)
                print(str(content))
        return contents

    def sentence_process(self, tags, mode):
        contents = list()
        se = Splitting()
        for tag in tags:
            contents = self.get_ariticles(tag, mode)
            for content in contents:
                results = se.split_article(content.get_content)
                self.set_sentences(content.get_id, results)
                self.update_article_scheck(content)

    def set_sentences(self, aid, sentences):
        cur = self.db.cursor()
        sql = ""
        for sentence in sentences:
            sql = "INSERT INTO sentence (aid, scontents, weight, wcheck) " \
                  "VALUES (%s, %s, 0, 0)"
            values = (aid, sentence)
            cur.execute(sql, values)
            self.db.commit()
            print("Sentence Insertion Success!\n[%s]" % str(sentence))

    def update_article_scheck(self, content):
        cur = self.db.cursor()
        sql = "UPDATE article SET scheck=1 WHERE aid=%s"
        values = (content.get_id)
        cur.execute(sql, values)
        self.db.commit()
        print("Update Article scheck Success!\n[%s]" % str(content))


if __name__ == "__main__":

    # cr = articleCrawler.Crawler()
    # result = cr.get_content(["http://news.naver.com/main/read.nhn?mode=LS2D&mid=sec&sid1=100&sid2=269&oid=009&aid=0003837948"], "정치")
    # print(result)
    # c.set_articles(result)
    c.sentence_process(["정치"], "s")




