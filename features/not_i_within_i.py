# -*- coding: utf-8 -*-
"""
A class that represents the not i-within-i Feature
"""

from abstract_feature import AbstractMentionFeature


class NotIWithinI(AbstractMentionFeature):

    def has_feature(self, mention1, mention2):
        # A i within i construction can only appear in same sentence.
        if mention1.index() == mention2.index():
            # Assuming well formed syntax trees, a mention is
            # within the constituent of another mention
            # if their spans overlap.
            start1, end1 = mention1.span()
            start2, end2 = mention2.span()
            if start1 <= end2 and end1 >= start2:
                return False
        return True
