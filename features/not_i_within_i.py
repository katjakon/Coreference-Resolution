# -*- coding: utf-8 -*-
"""
A class that represents the not i-within-i Feature
"""

from features.abstract_feature import AbstractMentionFeature


class NotIWithinI(AbstractMentionFeature):

    def has_feature(self, clusters, antecedent, mention):
        ant_cluster = clusters[antecedent]
        # A i within i construction can only appear in same sentence.
        for ant in ant_cluster:
            if mention.index() == ant.index():
                # Assuming well formed syntax trees, a mention is
                # within the constituent of another mention
                # if their spans overlap.
                start1, end1 = mention.span()
                start2, end2 = ant.span()
                if start1 <= end2 and end1 >= start2:
                    return False
        return True
