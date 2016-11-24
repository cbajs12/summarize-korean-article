# -*- coding: utf-8 -*-
import pymysql
import os
import sys
from articleCrawler import Crawler
from articleDTO import Article
from sentenceDTO import Sentence
from awordDTO import Awords
from swordDTO import Swords
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

    def article_process(self, specific_sector, days):
        """
        Crawling articles and save them to DB

        Args:
            specific_sector: list of crawling tags
            days: crawling data from days to today
        """
        cr = Crawler()

        sids = list()
        urls = list()
        contents = list()
        if specific_sector.__len__() == 0:
            sids = ["IT", "경제", "정치", "사회", "생활", "세계", "연예", "스포츠", "오피니언"]
        else:
            sids = specific_sector

        if days is None:
            days = 1

        for sid in sids:
            urls = cr.get_url(days, sid)
            urls = cr.get_news(urls)
            contents = cr.get_content(urls, sid)
            self.set_articles(contents)

    def article_process_url(self, url, tag):
        """
        Crawling specific url article and save it to DB

        Args:
            url: list of crawling tags
            tag: tag of article
        """
        cr = Crawler()
        contents = cr.get_single_news(url, tag)
        if contents is None:
            print("Content is None")
            exit()

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

    def get_articles(self, tag, mode):
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
        cur.execute(sql, values)        # self.db.commit()
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

    def get_awords(self, aid):
        """
        Get words from DB according to article id

        Args:
            aid : article id

        Returns: list of awords DTOs
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM awords WHERE aid=%s"""
        values = (aid)
        contents = list()
        cur.execute(sql, values)  # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        if total < 1:
            print('No Words')
        else:
            for record in range(total):
                content = Awords()
                content.set_id(row[record][0])
                content.set_aid(row[record][1])
                content.set_word(row[record][2].decode('utf8', 'surrogatepass'))
                content.set_count(row[record][3])
                contents.append(content)
                print(str(content))
        return contents

    def sentence_process(self, tags, mode):
        """
        Split article to sentences and save them to DB

        Args:
            tags: wanted tags for splitting
            mode: sentence or word
        """
        contents = list()
        for tag in tags:
            contents = self.get_articles(tag, mode)
            if mode == "s":
                se = Splitting("k")
                for content in contents:
                    results = se.split_article_to_sentence(content.get_content)
                    self.set_sentences(content.get_id, results)
                    self.update_article_scheck(content)
            elif mode == "w":
                se = Splitting("h")
                for content in contents:
                    temp = se.split_text_to_words(content.get_content)
                    results = se.check_duplicates_in_words(temp)
                    self.set_awords(content.get_id, results)
                    self.update_article_wcheck(content)

    def set_sentences(self, aid, sentences):
        """
        Save sentences to DB

        Args:
            aid: article id
            sentences: list of sentences
        """
        cur = self.db.cursor()
        sql = ""
        for sentence in sentences:
            sql = "INSERT INTO sentence (aid, scontents, weight, wcheck) " \
                  "VALUES (%s, %s, 0, 0)"
            values = (aid, sentence)
            cur.execute(sql, values)
            self.db.commit()
            print("Sentence Insertion Success!\n[%s]" % str(sentence))

    def set_awords(self, aid, words):
        """
        Save words of article to DB

        Args:
            aid: article id
            words: dictionary of words
        """
        cur = self.db.cursor()
        sql = ""
        for key, value in words.items():
            sql = "INSERT INTO awords (aid, awords, acounts) " \
                  "VALUES (%s, %s, %s)"
            values = (aid, key, value)
            cur.execute(sql, values)
            self.db.commit()
            print("Awords Insertion Success!\n[%s]" % str(key))

    def update_article_scheck(self, content):
        """
        Update scheck flag of article table

        Args:
            content: article DTO
        """
        cur = self.db.cursor()
        sql = "UPDATE article SET scheck=1 WHERE aid=%s"
        values = (content.get_id)
        cur.execute(sql, values)
        self.db.commit()
        print("Update Article scheck Success!\n[%s]" % str(content))

    def update_article_wcheck(self, content):
        """
        Update wcheck flag of article table

        Args:
            content: article DTO
        """
        cur = self.db.cursor()
        sql = "UPDATE article SET wcheck=1 WHERE aid=%s"
        values = (content.get_id)
        cur.execute(sql, values)
        self.db.commit()
        print("Update Article wcheck Success!\n[%s]" % str(content))

    def get_sentences(self, aid):
        """
        Get sentences from DB according to article id

        Args:
            aid: article id

        Returns: list of sentence DTOs
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM sentence WHERE aid=%s AND wcheck=0"""
        values = (aid)

        contents = list()
        cur.execute(sql, values)    # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        if total < 1:
            print('No Sentences')
        else:
            for record in range(total):
                content = Sentence()
                content.set_id(row[record][0])
                content.set_aid(row[record][1])
                content.set_content(row[record][2].decode('utf8', 'surrogatepass'))
                content.set_weight(row[record][3])
                content.set_wcheck(row[record][4])
                contents.append(content)
                print(str(content))
        return contents

    def get_sentences_all(self):
        """
        Get sentences from DB

        Returns: list of sentence DTOs
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM sentence WHERE wcheck=0"""

        contents = list()
        cur.execute(sql)  # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        if total < 1:
            print('No Sentences')
        else:
            for record in range(total):
                content = Sentence()
                content.set_id(row[record][0])
                content.set_aid(row[record][1])
                content.set_content(row[record][2].decode('utf8', 'surrogatepass'))
                content.set_weight(row[record][3])
                content.set_wcheck(row[record][4])
                contents.append(content)
                print(str(content))
        return contents

    def swords_process(self, aid):
        """
        Split sentence to words and save them to DB according to article id

        Args:
            aid: article id
        """
        se = Splitting("h")
        contents = self.get_sentences(aid)
        for content in contents:
            temp = se.split_text_to_words(content.get_content)
            results = se.check_duplicates_in_words(temp)
            self.set_swords(content.get_id, content.get_aid, results)
            self.update_sentence_wcheck(content)

    def swords_process_all(self):
        """
        Split sentence to words and save them to DB
        """
        se = Splitting("h")
        contents = self.get_sentences_all()
        for content in contents:
            temp = se.split_text_to_words(content.get_content)
            results = se.check_duplicates_in_words(temp)
            self.set_swords(content.get_id, content.get_aid, results)
            self.update_sentence_wcheck(content)

    def set_swords(self, sid, aid, words):
        """
        Save words of sentence to DB

        Args:
            sid: sentence id
            aid: article id
            words: dictionary of words
        """
        cur = self.db.cursor()
        sql = ""
        for key, value in words.items():
            sql = "INSERT INTO swords (swords, aid, sid, scounts) " \
                  "VALUES (%s, %s, %s, %s)"
            values = (key, aid, sid, value)
            cur.execute(sql, values)
            self.db.commit()
            print("Swords Insertion Success!\n[%s]" % str(key))

    def update_sentence_wcheck(self, content):
        """
        Update wcheck flag of sentence table

        Args:
            content: sentence DTO
        """
        cur = self.db.cursor()
        sql = "UPDATE sentence SET wcheck=1 WHERE sid=%s"
        values = (content.get_id)
        cur.execute(sql, values)
        self.db.commit()
        print("Update Sentence wcheck Success!\n[%s]" % str(content))

    def get_swords(self, sid):
        """
        Get words from DB according to sentence id

        Args:
            sid: sentence id

        Returns: list of swords DTOs
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM swords WHERE sid=%s"""
        values = (sid)

        contents = list()
        cur.execute(sql, values)  # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        if total < 1:
            print('No Words')
        else:
            for record in range(total):
                content = Swords()
                content.set_id(row[record][0])
                content.set_word(row[record][1].decode('utf8', 'surrogatepass'))
                content.set_aid(row[record][2])
                content.set_sid(row[record][3])
                content.set_count(row[record][4])
                contents.append(content)
                print(str(content))
        return contents

    def get_swords_count(self, sid):
        """
        Get words count from DB according to sentence id

        Args:
            sid: sentence id

        Returns: count of words
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM swords WHERE sid=%s"""
        values = (sid)

        cur.execute(sql, values)  # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        return total

    def get_processed_sentences(self, aid):
        """
        Get sentences which wcheck is 1 and specific article from DB

        Args:
            aid: article id

        Returns: list of sentence DTOs
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM sentence WHERE wcheck=1 AND aid=%s"""
        values = (aid)

        contents = list()
        cur.execute(sql, values)  # self.db.commit()
        row = cur.fetchall()
        total = len(row)

        if total < 1:
            print('No Sentences')
        else:
            for record in range(total):
                content = Sentence()
                content.set_id(row[record][0])
                content.set_aid(row[record][1])
                content.set_content(row[record][2].decode('utf8', 'surrogatepass'))
                content.set_weight(row[record][3])
                content.set_wcheck(row[record][4])
                contents.append(content)
                print(str(content))
        return contents


if __name__ == "__main__":
    print("hi")
    # cr = articleCrawler.Crawler()
    # print(result)
    # c.set_articles(result)
    # c.get_sentences(1)
    # c.swords_process(1)
    # c.sentence_process(["정치"], "w")



