# -*- coding: utf-8 -*-


class Sentence:
    def __init__(self, aid="", content=""):
        self.sid = 0
        self.aid = aid
        self.content = content
        self.weight = 0
        self.wcheck = 0

    @property
    def get_id(self):
        return self.sid

    def set_id(self, sid):
        self.sid = sid

    @property
    def get_aid(self):
        return self.aid

    def set_aid(self, aid):
        self.aid = aid

    @property
    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content

    @property
    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    @property
    def get_wcheck(self):
        return self.wcheck

    def set_wcheck(self, wcheck):
        self.wcheck = wcheck

    def __str__(self):
        return "Sentence [sid=" + str(self.sid) + ", aid=" + str(self.aid) + " content=" + str(self.content) + \
               ", weight=" + str(self.weight) + ", wcheck=" + str(self.get_wcheck) + "]"
