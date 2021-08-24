# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 11:34:09 2021

@author: HP I5
"""
from features.abstract_feature import AbstractMentionFeature


class CompatibleModifiersOnly(AbstractMentionFeature):

    def __init__(self, modifiers={"JJ", "JJR", "JJS", "NN", "NNP", "NNS"}):
        self.modifiers = modifiers

    def has_feature(self, antecedent, mention):
        mod_ant = self._extract_modifiers(antecedent)
        mod_ment = self._extract_modifiers(mention)
        if mod_ment.issubset(mod_ant):
            return True
        return False

    def _extract_modifiers(self, mention):
        pos = mention.pos
        head = mention.head
        modifiers = set()
        for token, pos in pos:
            if pos in self.modifiers and token != head:
                modifiers.add(token)
        return modifiers
