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

    def split_text_to_words(self, text):
        """
        Split text to words

        Args:
            text: text string

        Returns: list of words
        """
        words = list()
        if self.mode == "t":
            words = self.twitter.nouns(text)
        elif self.mode == "k":
            words = self.kkma.nouns(text)
        elif self.mode == "h":
            words = self.hannaum.nouns(text)
        elif self.mode == "ko":
            words = self.komoran.nouns(text)
        elif self.mode == "m":
            words = self.mecab.nouns(text)

        print(words)
        return words

    def check_duplicates_in_words(self, words):
        """
        Eliminate duplicated words and count them
        Args:
            words: list of words

        Returns: dictionary of word and count

        """
        results = dict()

        for word in words:
            temp = results.get(word)
            if temp is None:
                results[word] = 1
            else:
                results[word] += 1

        print(results)
        return results


if __name__ == "__main__":
    ar = "이화여대 교수들은 입학 전형 과정에서 정씨를 위해 서류평가 상위점수 학생들의 면접 점수를 조정했고"
    sh = Splitting("h")

    print("h")
    b = sh.split_text_to_words(ar)
    sh.check_duplicates_in_words(b)

