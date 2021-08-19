# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 11:34:09 2021

@author: HP I5
"""
import re

from features.abstract_feature import AbstractMentionFeature


class CompatibleModifiersOnly(AbstractMentionFeature):

    def __init__(self, modifiers=(r"JJ[R|S]?", r"NNP?S?")):
        self.modifiers = modifiers

    def has_feature(self, antecedent, mention):
        mod_ant = self._extract_modifiers(antecedent)
        mod_ment = self._extract_modifiers(mention)
        if mod_ment.issubset(mod_ant):
            return True
        return False

    def _extract_modifiers(self, mention):
        pos = mention.tree.pos()
        head = mention.head()
        modifiers = set()
        for token, pos in pos:
            for mod in self.modifiers:
                if re.match(mod, pos) and token != head:
                    modifiers.add(token)
        return modifiers
