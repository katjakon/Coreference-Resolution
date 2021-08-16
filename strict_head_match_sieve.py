# -*- coding: utf-8 -*-
"""
Strict Head Matching Sieve
"""

from abstract_sieve import AbstractSieve
from features.abstract_feature import AbstractMentionFeature, AbstractClusterFeature
from features.cluster_head_match import ClusterHeadMatch
from features.compatible_modifiers_only import CompatibleModifiersOnly
from features.not_i_within_i import NotIWithinI
from features.word_inclusion import WordInclusion


class StrictHeadMatchSieve(AbstractSieve):

    def __init__(self, lang="english", modifiers=(r"JJ[R|S]?", r"NNP?S?")):
        self.cluster_features = [ClusterHeadMatch(),
                                 WordInclusion(lang)]
        self.mention_features = (NotIWithinI(),
                                 CompatibleModifiersOnly(modifiers))

    def resolve(self, cluster):
        unresolved = cluster.unresolved()
        for mention in unresolved:
            if not mention.pronominal() and not mention.indefinite():
                same_sent, prev_sent = cluster.antecedents(mention)
                all_ant = same_sent + prev_sent
                for antecedent in all_ant:
                    has_cluster_feat = all((feat.has_feature(cluster,
                                                             antecedent,
                                                             mention)
                                           for feat in self.cluster_features))
                    has_mention_feat = all((feat.has_feature(antecedent,
                                                             mention)
                                           for feat in self.mention_features))
                    if has_mention_feat and has_cluster_feat:
                        cluster.merge(antecedent, mention)
                        break
