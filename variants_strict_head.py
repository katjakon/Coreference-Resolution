# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:43:19 2021

@author: HP I5
"""

from strict_head_match_sieve import StrictHeadMatchSieve
from features.abstract_feature import AbstractMentionFeature, AbstractClusterFeature
from features.cluster_head_match import ClusterHeadMatch
from features.compatible_modifiers_only import CompatibleModifiersOnly
from features.not_i_within_i import NotIWithinI
from features.word_inclusion import WordInclusion


class StrictHeadRelaxModifiers(StrictHeadMatchSieve):

    def __init__(self, lang="english"):
        self.cluster_features = (ClusterHeadMatch(),
                                 WordInclusion(lang))
        self.mention_features = (NotIWithinI(),)


class StrictHeadRelaxInclusion(StrictHeadMatchSieve):

    def __init__(self, modifiers=(r"JJ[R|S]?", r"NNP?S?")):
        self.cluster_features = (ClusterHeadMatch(),)
        self.mention_features = (NotIWithinI(),
                                 CompatibleModifiersOnly(modifiers))
