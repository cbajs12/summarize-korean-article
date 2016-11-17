# -*- coding: utf-8 -*-

from konlpy.tag import Kkma
from konlpy.tag import Twitter
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
from konlpy.tag import Mecab


class Splitting:
    def __init__(self, mode):
        """
        Initiate module according to mode

        Args:
            mode: twitter , kkma, hannanum, komoran or mecab
        """
        self.mode = mode
        if mode == "t":
            self.twitter = Twitter()
        elif mode == "k":
            self.kkma = Kkma()
        elif mode == "h":
            self.hannaum = Hannanum()
        elif mode == "ko":
            self.komoran = Komoran()
        elif mode == "m":
            self.mecab = Mecab()

    def split_article_to_sentence(self, content):
        """
        Split article to sentence

        Args:
            content: article string

        Returns: list of sentences
        """
        results = self.kkma.sentences(content)
        return results

    def split_sentence_to_words(self, sentence):
        """
        Split sentence to words

        Args:
            sentence: sentence string

        Returns: list of words
        """
        words = list()
        if self.mode == "t":
            words = self.twitter.nouns(sentence)
        elif self.mode == "k":
            words = self.kkma.nouns(sentence)
        elif self.mode == "h":
            words = self.hannaum.nouns(sentence)
        elif self.mode == "ko":
            words = self.komoran.nouns(sentence)
        elif self.mode == "m":
            words = self.mecab.nouns(sentence)

        print(words)
        return words

    def split_article_to_words(self, article):      # 어떤 것이 가장 효율이 좋은가
        """
        Split article to words

        Args:
            article: article string

        Returns: list of words
        """
        words = list()
        if self.mode == "t":
            words = self.twitter.nouns(article)
        elif self.mode == "k":
            words = self.kkma.nouns(article)
        elif self.mode == "h":
            words = self.hannaum.nouns(article)
        elif self.mode == "ko":
            words = self.komoran.nouns(article)
        elif self.mode == "m":
            words = self.mecab.nouns(article)

        print(words)
        return words

    # 중복되는 단어 카운팅해서 저장
    def check_duplicates_in_words(self, words):

        results = dict()

        return results


if __name__ == "__main__":
    print("a")
