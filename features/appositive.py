# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 21:35:17 2021

@author: HP I5
"""

class Appositive:

    def has_feature(self, antecedent, mention):
        ment_tree = mention.tree
        ant_tree = antecedent.tree
        # Possible only in same sentence.
        if antecedent.index() == mention.index():
            parent_ant = ant_tree.parent()
            parent_ment = ment_tree.parent()
            # We might reach the root by calling parent().
            if not (parent_ant is None or parent_ment is None):
                # This means they have the same parent.
                # By using "is" it is ensured parents are the same object,
                # and don't just appear the same.
                if parent_ant is parent_ment:
                    # We allow for an additional punctuation mark in children.
                    if len(parent_ant) <= 3:
                        appositive = True
                        for child in parent_ant:
                            is_ant = child is ant_tree
                            is_ment = child is ment_tree
                            is_punc = child.label() == ","
                            if not (is_ant or is_ment or is_punc):
                                appositive = False
                        if appositive:
                            return True
        return False
