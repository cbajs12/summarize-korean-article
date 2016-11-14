# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
import requests
import bs4
import time


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

    def get_url(self, days, specific_sector):
        """
        Get target article list urls
        Args:
            days: wanted article from days ago
            specific_sector: wanted sector list for crawling

        Returns: target article url list

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

        rotate = dict()
        if specific_sector.__len__() != 0:
            for s in specific_sector:
                rotate[s] = sid1s[s]
        else:
            rotate = sid1s

        urls = list()

        if rotate.__len__() == 0:
            return urls

        d = datetime.today()

        for i in range(days):
            article_date = self.change_date_format(d - timedelta(i))
            sid2 = None
            for s1 in rotate.keys():
                if s1 == "IT":
                    sid2 = sid2s_it
                elif s1 == "경제":
                    sid2 = sid2s_ec
                elif s1 == "정치":
                    sid2 = sid2s_po
                elif s1 == "사회":
                    sid2 = sid2s_so
                elif s1 == "생활":
                    sid2 = sid2s_lf
                elif s1 == "세계":
                    sid2 = sid2s_wo
                elif s1 == "연예":
                    sid2 = sid2s_en
                elif s1 == "스포츠":
                    sid2 = sid2s_sp

                url = "http://news.naver.com/main/list.nhn?mode=LS2D&mid=sec" + "&sid1=" + str(rotate[s1])
                print(url)
                if sid2 is not None:
                    for s2 in sid2.values():
                        url += "&sid2=" + str(s2) + "&date=" + article_date

                        pages = self.get_pages_count(url + "&page=1")
                        for page in range(pages):
                            final_url = url + "&page=" + str(page + 1)
                            urls.append(final_url)
                else:
                    pages = self.get_pages_count(url + "&page=1")
                    for page in range(pages):
                        final_url = url + "&page=" + str(page + 1)
                        urls.append(final_url)

        return urls

if __name__ == "__main__":
    target = ["정치", "세계"]
    result = Crawler().get_url(1, target)
    print(result)
