# -*- coding: utf-8 -*-


class Awords:
    def __init__(self, aid="", word="", count=""):
        self.awid = 0
        self.aid = aid
        self.word = word
        self.count = count

    @property
    def get_id(self):
        return self.awid

    def set_id(self, awid):
        self.awid = awid

    @property
    def get_aid(self):
        return self.aid

    def set_aid(self, aid):
        self.aid = aid

    @property
    def get_word(self):
        return self.word

    def set_word(self, word):
        self.word = word

    @property
    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def __str__(self):
        return "Sword [swid=" + str(self.awid) + ", aid=" + str(self.aid) + " word=" + str(
            self.word) + ", count=" + str(self.count) + "]"
