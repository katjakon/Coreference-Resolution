# -*- coding: utf-8 -*-
"""
A feature that determines if two mentions are acronyms of each other.
"""


class Acronyms:

    def __init__(self, tags=("NNP",)):
        self.tags = tags

    def has_feature(self, mention1, mention2):
        words1 = mention1.words
        words2 = mention2.words
        if self._is_proper(mention1) and self._is_proper(mention2):
            upper1 = self._upper_letters(words1)
            upper2 = self._upper_letters(words2)
            if words1 == upper2 or words2 == upper1:
                return True
            return False

    def _is_proper(self, mention):
        return all(pos in self.tags for _, pos in mention.pos)

    def _upper_letters(self, words):
        upper = (letter for w in words for letter in w if letter.isupper())
        return ["".join(upper)]
