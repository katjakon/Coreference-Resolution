# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 20:43:56 2021

@author: HP I5
"""

from abstract_sieve import AbstractSieve
from features.acronym import Acronyms
from features.appositive import Appositive
from features.predicate_nominative import PredicateNominative


class PreciseConstructsSieve(AbstractSieve):

    def __init__(self, predicate={"be"}):
        self.cluster_features = (PredicateNominative(),)
        self.mention_features = (Acronyms(),
                                 Appositive())
        

    def resolve(self, clusters):
        unresolved = clusters.unresolved()
        for mention in unresolved:
            if not mention.indefinite:
                for ant in clusters.antecedents(mention):
                    if not ant.indefinite:
                        any_feat = False
                        for feat in self.cluster_features:
                            if feat.has_feature(clusters, ant, mention):
                                any_feat = True
                        for feat in self.mention_features:
                            if feat.has_feature(ant, mention):
                                any_feat = True
                        if any_feat:
                            clusters.merge(ant, mention)
                            break
