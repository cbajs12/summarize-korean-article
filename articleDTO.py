# -*- coding: utf-8 -*-


class Article:
    def __init__(self, title="", content="", tag="", sub_tag=""):
        self.aid = 0
        self.title = title
        self.content = content
        self.tag = tag
        self.sub_tag = sub_tag
        self.scheck = 0
        self.wcheck = 0

    @property
    def get_id(self):
        return self.aid

    def set_id(self, aid):
        self.aid = aid

    @property
    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    @property
    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content

    @property
    def get_tag(self):
        return self.tag

    def set_tag(self, tag):
        self.tag = tag

    @property
    def get_sub_tag(self):
        return self.sub_tag

    def set_sub_tag(self, sub_tag):
        self.sub_tag = sub_tag

    @property
    def get_scheck(self):
        return self.scheck

    def set_scheck(self, scheck):
        self.scheck = scheck

    @property
    def get_wcheck(self):
        return self.wcheck

    def set_wcheck(self, wcheck):
        self.wcheck = wcheck

    def __str__(self):
        return "Article [id = " + str(self.aid) + ", title=" + str(self.title) + " content=" + str(self.content) + ", tag=" + str(
            self.tag) + ", sugtag=" + str(self.sub_tag) + ", scheck=" + str(self.get_scheck) + \
               ", wcheck=" + str(self.get_wcheck) + "]"

