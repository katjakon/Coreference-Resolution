# -*- coding: utf-8 -*-
"""
A feature that represents the Cluster Head Matching
"""

from features.abstract_feature import AbstractClusterFeature


class ClusterHeadMatch(AbstractClusterFeature):

    def has_feature(self, cluster, antecedent, mention):
        head_ment = mention.head
        cluster_ant = cluster[antecedent]
        heads_ant = {mention.head for mention in cluster_ant}
        if head_ment in heads_ant:
            return True
        return False
