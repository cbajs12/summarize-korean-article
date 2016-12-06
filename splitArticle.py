# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
from konlpy.tag import Mecab
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


class Splitting:
    def __init__(self, mode=None):
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

        if self.mode is not None:
            results = self.kkma.sentences(content)
        else:
            results = sent_tokenize(content)
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
        elif self.mode is None:
            tokenizer = RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(text)

        # print(words)
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

        # print(results)
        return results


if __name__ == "__main__":
    ar = "By John RedmondThe Camarata Music Company Chorale (CMC) and Orchestra will perform its annual holiday concert of Handel’s “Messiah” at Chungdong First Methodist Church, central Seoul, Saturday.The performance will feature the Camarata Chorale, an amateur singing group.Conductor Dr. Ryan Goessl will perform with special guests, including soloists Oh Shin-young, Nam Jung-hee (mezzo-soprano), Hong Myoung-po (tenor) and Seong Seung-wook (bass).The event will also feature a pre-concert Christmas performance from the Camarata Children’s Choir.The CMC is a nonprofit organization that presents opportunities for the public to hear classical music performed by people from many different cultures and nationalities."
    sh = Splitting()
    #
    print("h")
    b = sh.split_text_to_words(ar)
    sh.check_duplicates_in_words(b)

