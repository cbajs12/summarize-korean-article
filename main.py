# -*- coding: utf-8 -*-
from controller import Controller

if __name__ == "__main__":
    print("use celery")
    print("use spark")
    print("make various weight process")
    print("refactor of article crawling")

    print("Choose Mode\n")
    print("1. Crawling news for specific days ago or 2. Crawling specific news")
    select = input("Write 1 or 2 \n")


    sector = ["정치"]

    if select == 1:
        # crawling
        days = input("Input days \n")
        c.article_process(sector, days)
    elif select == 2:
        # crawling
        url = input("Input specific news url")
        c.article_process_url(url, sector)
    else:
        print("Wrong input")
        exit()

    # article to sentences
    c.sentence_process(sector, "s")

    # article to words
    c.sentence_process(sector, "w")

    # sentences to words
    c.swords_process_all()

    # pre-processing
    # fuzzy algorithm
    # result





