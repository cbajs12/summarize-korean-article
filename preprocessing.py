# -*- coding: utf-8 -*-
from controller import Controller
from sentenceDTO import Sentence


class Processing:
    def length_per_words(self, controller, aid):
        sentences = controller.get_processed_sentences(aid)

        for s in sentences:
            content = s.get_content
            length = len(content)
            word_count = controller.get_swords(s.get_id)


if __name__ == "__main__":
    print("hi")
