# -*- coding: utf-8 -*-


class Swords:
    def __init__(self, aid="", sid="", word="", count=""):
        self.swid = 0
        self.aid = aid
        self.sid = sid
        self.word = word
        self.count = count

    @property
    def get_id(self):
        return self.swid

    def set_id(self, swid):
        self.swid = swid

    @property
    def get_aid(self):
        return self.aid

    def set_aid(self, aid):
        self.aid = aid

    @property
    def get_sid(self):
        return self.sid

    def set_sid(self, sid):
        self.sid = sid

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
        return "Sword [swid=" + str(self.swid) + ", sid=" + str(self.sid) + ", aid=" + str(self.aid) + " word=" + str(self.word) + \
               ", count=" + str(self.count) + "]"
