# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import requests
import bs4
import urllib.parse as urlparse
from articleDTO import Article
import re


class Crawler:
    def get_date_from_news(self, article_date):
        """
        Get date from article and chage its format(YYYY-MM-DD) to YYYYMMDD format

        Args:
            article_date: article date format (YYYY-MM-DD)

        Returns: changed date format (YYYYMMDD)
        """
        year = article_date[0:4]
        month = article_date[5:7]
        day = article_date[8:10]
        return "" + year + month + day

    def change_date_format(self, d):
        """
        Change datetime format to YYYYMMDD format

        Args:
            d: datetime data

        Returns: YYYYMMDD format data
        """
        today = str(d.year)
        mon = ""
        if len(str(d.month)) < 2:
            mon = "0" + str(d.month)
        else:
            mon = str(d.month)

        today += mon
        day = ""

        if len(str(d.day)) < 2:
            day = "0" + str(d.day)
        else:
            day = str(d.day)

        today += day

        return today

    def get_pages_count(self, url):
        """
        Counting pages of articles

        Args:
            url: get article

        Returns: counts
        """
        res = requests.get(url)
        html_content = res.text
        navigator = bs4.BeautifulSoup(html_content, 'html5lib')  # lxml
        pages = navigator.find("div", {"class": "paging"})
        if pages is not None:
            page_nums = pages.find_all('a')
            page_num = [item.get_text() for item in page_nums]
            return 1 + len(page_num)
        return 1

    def get_url(self, days, sid):
        """
        Get target article list urls

        Args:
            days: wanted article from days ago
            sid: Specific tag for crawling

        Returns: target article url dict
        """
        sid1s = {"IT": 105, "경제": 101, "정치": 100, "사회": 102, "생활": 103, "세계": 104, "연예": 106, "스포츠": 107, "오피니언": 110}
        sid2s_it = {"인터넷/SNS": 226, "IT일반": 230, "보안/해킹": 732, "컴퓨터": 283,
                    "게임/리뷰": 229, "과학 일반": 228}
        sid2s_ec = {"금융": 259, "증권": 258, "산업/재계": 261, "중기/벤쳐": 771,
                    "부동산": 260, "글로벌경제": 262, "경제일반": 263}
        sid2s_so = {"사건사고": 249, "교육": 250, "노동": 251, "환경": 252, "언론": 254, "지역": 256, "인물": 276, "사회일반": 257}
        sid2s_po = {"청와대": 264, "국회/정당": 265, "행정": 266, "국방/외교": 267, "북한": 268, "정치일반": 269}
        sid2s_lf = {"여행/레저": 237, "자동차/시승기": 239, "도로/교통": 240, "건강정보": 241, "공연/전시": 242,
                    "책": 243, "종교": 244, "생활일반": 245}
        sid2s_wo = {"아시아/호주": 231, "미국/중남미": 232, "유럽": 233, "중동/아프리카": 234, "영문": "64f", "일문": "71a"}
        sid2s_sp = {"국내야구": 781, "해외야구": 784, "국내축구": 787, "해외축구": "77a",
                    "농구": "78b", "배구": 790, "골프": 792, "종합": 794, "e스포츠": "79a"}
        sid2s_en = {"연예가화제": 221, "방송/TV": 224, "드라마": 225, "영화": 222, "해외연예": 309}

        d = datetime.today()
        l = list()

        for i in range(days):
            article_date = self.change_date_format(d - timedelta(i))
            sid2 = None

            if sid == "IT":
                sid2 = sid2s_it
            elif sid == "경제":
                sid2 = sid2s_ec
            elif sid == "정치":
                sid2 = sid2s_po
            elif sid == "사회":
                sid2 = sid2s_so
            elif sid == "생활":
                sid2 = sid2s_lf
            elif sid == "세계":
                sid2 = sid2s_wo
            elif sid == "연예":
                sid2 = sid2s_en
            elif sid == "스포츠":
                sid2 = sid2s_sp

            url = "http://news.naver.com/main/list.nhn?mode=LS2D&mid=sec" + "&sid1=" + str(sid1s[sid])
            l = list()
            if sid2 is not None:
                for key, values in sid2.items():
                    mid_url = url + "&sid2=" + str(values) + "&date=" + article_date

                    pages = self.get_pages_count(mid_url + "&page=1")
                    for page in range(pages):
                        final_url = mid_url + "&page=" + str(page + 1)
                        l.append(final_url)

            else:
                pages = self.get_pages_count(url + "&page=1")
                for page in range(pages):
                    final_url = url + "&page=" + str(page + 1)
                    l.append(final_url)

        return l

    def get_url_special(self, days, sid, name):
        """
        Get target article list urls

        Args:
            days: wanted article from days ago
            sid: Specific tag for crawling
            name: name of specific sid2

        Returns: target article url dict
        """
        sid1s = {"IT": 105, "경제": 101, "정치": 100, "사회": 102, "생활": 103, "세계": 104, "연예": 106, "스포츠": 107, "오피니언": 110}
        sid2s_it = {"인터넷/SNS": 226, "IT일반": 230, "보안/해킹": 732, "컴퓨터": 283,
                    "게임/리뷰": 229, "과학 일반": 228}
        sid2s_ec = {"금융": 259, "증권": 258, "산업/재계": 261, "중기/벤쳐": 771,
                    "부동산": 260, "글로벌경제": 262, "경제일반": 263}
        sid2s_so = {"사건사고": 249, "교육": 250, "노동": 251, "환경": 252, "언론": 254, "지역": 256, "인물": 276, "사회일반": 257}
        sid2s_po = {"청와대": 264, "국회/정당": 265, "행정": 266, "국방/외교": 267, "북한": 268, "정치일반": 269}
        sid2s_lf = {"여행/레저": 237, "자동차/시승기": 239, "도로/교통": 240, "건강정보": 241, "공연/전시": 242,
                    "책": 243, "종교": 244, "생활일반": 245}
        sid2s_wo = {"아시아/호주": 231, "미국/중남미": 232, "유럽": 233, "중동/아프리카": 234, "영문": "64f", "일문": "71a"}
        sid2s_sp = {"국내야구": 781, "해외야구": 784, "국내축구": 787, "해외축구": "77a",
                    "농구": "78b", "배구": 790, "골프": 792, "종합": 794, "e스포츠": "79a"}
        sid2s_en = {"연예가화제": 221, "방송/TV": 224, "드라마": 225, "영화": 222, "해외연예": 309}

        d = datetime.today()
        l = list()

        for i in range(days):
            article_date = self.change_date_format(d - timedelta(i))
            sid2 = None
            if sid == "IT":
                temp = sid2s_it[name]
                sid2 = temp
            elif sid == "경제":
                temp = sid2s_ec[name]
                sid2 = temp
            elif sid == "정치":
                temp = sid2s_po[name]
                sid2 = temp
            elif sid == "사회":
                temp = sid2s_so[name]
                sid2 = temp
            elif sid == "생활":
                temp = sid2s_lf[name]
                sid2 = temp
            elif sid == "세계":
                temp = sid2s_wo[name]
                sid2 = temp
            elif sid == "연예":
                temp = sid2s_en[name]
                sid2 = temp
            elif sid == "스포츠":
                temp = sid2s_sp[name]
                sid2 = temp

            url = "http://news.naver.com/main/list.nhn?mode=LS2D&mid=sec" + "&sid1=" + str(sid1s[sid])
            l = list()
            if sid2 is not None:
                mid_url = url + "&sid2=" + str(sid2) + "&date=" + article_date

                pages = self.get_pages_count(mid_url + "&page=1")
                for page in range(pages):
                    final_url = mid_url + "&page=" + str(page + 1)
                    l.append(final_url)
            else:
                pages = self.get_pages_count(url + "&page=1")
                for page in range(pages):
                    final_url = url + "&page=" + str(page + 1)
                    l.append(final_url)

        return l

    def get_url_naver_en(self, days):
        """
        Get target article list urls

        Args:
            days: wanted article from days ago

        Returns: target article url dict
        """

        sid = "104"
        sid2 = "64f"
        sid3 = "657"        # (politics) 658(special) 656(business) 209(tech) 654(art) 653(sports) 652(opinion)

        d = datetime.today()
        l = list()

        for i in range(days):
            article_date = self.change_date_format(d - timedelta(i))

            url = "http://news.naver.com/main/list.nhn?mode=LS3D&mid=sec" + "&sid1=" + sid + "&sid2=" + \
                  sid2 + "&sid3=" + sid3

            l = list()
            mid_url = url + "&date=" + article_date

            pages = self.get_pages_count(mid_url + "&page=1")
            for page in range(pages):
                final_url = mid_url + "&page=" + str(page + 1)
                l.append(final_url)

        return l

    def get_news(self, urls):
        """
        Get article urls from article paging urls

        Args:
            urls: list of article paging urls

        Returns: list of article urls
        """
        url_lists = list()

        for url in urls:
            res = requests.get(url)
            html_content = res.text
            navigator = bs4.BeautifulSoup(html_content, 'html5lib')

            headlines = navigator.find("ul", {"class": "type06_headline"})

            if headlines is not None:
                headline = headlines.find_all("dt")
                result_list = [item.a for item in headline]

            normals = navigator.find("ul", {"class": "type06"})

            if normals is not None:
                normal = normals.find_all("dt")
                for item in normal:
                    result_list.append(item.a)

            url_lists = url_lists + [item['href'] for item in result_list]

            url_lists = list(set(url_lists))    # remove duplicates
            # time.sleep(0.000001)

        # for index, url_list in enumerate(url_lists):
        #     result_text = '[%d개] %s' % (index + 1, url_list)
        #     print(result_text)

        return url_lists

    def get_single_news(self, url, tag):
        """
        Get article contents from article url

        Args:
            url: article url
            tag: article tag

        Returns: list of article DTO
        """
        results = list()

        sub_tag = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))["sid2"]

        # print(url)
        res = requests.get(url)
        html_content = res.text
        navigator = bs4.BeautifulSoup(html_content, 'html5lib')

        contents = navigator.find("div", id="main_content")
        header = contents.h3.get_text().strip().replace("\"\r\n\t", '')

        text = ""
        content = contents.find("div", id="articleBodyContents")
        # print(content)
        if content.find("table") is None:
            text = content.get_text()
        else:
            return None

        if text == "":
            print("Text is empty")
            return None

        text = text.strip().replace("\"\r\n\t", '')

        article = Article()
        article.set_title(header)
        article.set_content(text)
        article.set_tag(tag)
        article.set_sub_tag(sub_tag)
        results.append(article)
        print(str(article) + ' Original')
        return results

    def get_content(self, urls, tag):
        """
        Get article contents from article urls

        Args:
            urls: article urls
            tag: article tag

        Returns: list of article DTOs
        """
        results = list()

        for url in urls:
            sub_tag = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))["sid2"]

            # print(url)
            res = requests.get(url)
            html_content = res.text
            navigator = bs4.BeautifulSoup(html_content, 'html5lib')

            contents = navigator.find("div", id="main_content")
            header = contents.h3.get_text().strip().replace("\"\r\n\t", '')

            text = ""
            content = contents.find("div", id="articleBodyContents")
            print(content)
            if content.find("table") is None:
                text = content.get_text()
            else:
                continue

            if text == "":
                continue

            text = text.strip().replace("\"\r\n\t", '')

            article = Article()
            article.set_title(header)
            article.set_content(text)
            article.set_tag(tag)
            article.set_sub_tag(sub_tag)
            results.append(article)
            # print(str(article) + ' Original')
        return results

    def get_content_en(self, urls, tag):
        """
        Get article contents from article urls

        Args:
            urls: article urls
            tag: article tag

        Returns: list of article DTOs
        """
        results = list()

        for url in urls:
            sub_tag = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))["sid2"]

            # print(url)
            res = requests.get(url)
            html_content = res.text

            navigator = bs4.BeautifulSoup(html_content, 'html5lib')

            contents = navigator.find("div", id="main_content")
            header = contents.h3.get_text().strip().replace("\"\r\n\t", '')

            text = ""
            content = contents.find("div", id="articleBodyContents")

            if content.find("table") is None:
                text = content.get_text()
            else:
                continue

            if text == "":
                continue

            [s.extract() for s in content(['style', 'script', '[document]', 'head', 'title'])]
            text = content.get_text().strip()

            article = Article()
            article.set_title(header)
            article.set_content(text)
            article.set_tag(tag)
            article.set_sub_tag(sub_tag)
            results.append(article)
            # print(str(article) + ' Original')
        return results

if __name__ == "__main__":
    c = Crawler()
    a = c.get_url_naver_en(1)
    print(a)
    d = c.get_news(a)
