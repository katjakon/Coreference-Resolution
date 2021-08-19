# -*- coding: utf-8 -*-
"""
A feature that determines if two mentions are acronyms of each other.
"""


class Acronyms:

    def has_feature(self, mention1, mention2):
        words1 = mention1.words
        words2 = mention2.words
        if self._upper_letters(words1) == self._upper_letters(words2):
            return True
        return False

    def _upper_letters(self, words):
        upper = []
        for word in words:
            for letter in word:
                if letter.isupper():
                    upper.append(letter)
        return upper
