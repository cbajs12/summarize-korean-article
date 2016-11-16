# -*- coding: utf-8 -*-

from konlpy.tag import Kkma


class Splitting:
    def __init__(self):
        self.kkma = Kkma()

    def split_article(self, content):
        results = self.kkma.sentences(content)
        return results
