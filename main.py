# -*- coding: utf-8 -*-
from controller import Controller

if __name__ == "__main__":
    # print("use celery")
    # print("use spark")
    # print("make various weight process")
    # print("refactor of article crawling")

    print("Naver article analyzer\n")
    print("Choose Mode\n")
    print("1. Crawling specific sector news for specific days ago")
    print("2. Crawling specific news with url\n")
    print("3. Crawling specific sector news with specific topic for specific days ago \n")
    print("4. Crawling Naver english article")
    select = input("Choose One\n")

    # c = Controller("username", "password", "instance_name", "host_address")

    sector = ["세계"]

    sid2 = "영문"

    if select == 1:
        # crawling
        days = input("Input days \n")
        c.article_process(days, sector)
    elif select == 2:
        # crawling
        url = input("Input specific news url")
        c.article_process_url(url, sector)
    elif select == 3:
        # crawling
        days = input("Input days \n")
        c.article_process(days, sector, sid2)
    elif select == 4:
        # crawling
        days = input("Input days \n")
        c.article_process(days, "en")
    else:
        print("Wrong input")
        exit()

    # if sid2 is None:              # specific sid2 & language process
    #     # article to sentences
    #     c.sentence_process(sector, "s", "kr")
    #
    #     # article to words
    #     c.sentence_process(sector, "w", "kr")
    # else:
    #     # article to sentences
    #     c.sentence_process(sector, "s", "en")
    #
    #     # article to words
    #     c.sentence_process(sector, "w", "en")

    # article to sentences
    c.sentence_process(sector, "s", "en")

    # article to words
    c.sentence_process(sector, "w", "en")

    # sentences to words
    c.swords_process_sentence("en")

    # pre-processing
    # fuzzy algorithm
    # result





