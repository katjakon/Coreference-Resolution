# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 21:35:17 2021

@author: HP I5
"""


class Appositive:

    def __init__(self, allowed_labels=(",",), allowed_len=3):
        self.allowed_labels = allowed_labels
        if allowed_len < 2:
            raise Exception("Appostive Construction "
                            "must allow at least 2 children.")
        self.allowed_len = allowed_len

    def has_feature(self, antecedent, mention):
        ment_tree = mention.tree
        ant_tree = antecedent.tree
        # Possible only in same sentence.
        if antecedent.index() == mention.index():
            parent_ant = ant_tree.parent()
            parent_ment = ment_tree.parent()
            # We might be at the root when calling parent().
            if not (parent_ant is None or parent_ment is None):
                # This means they have the same parent.
                # By using "is" it is ensured parents are the same object,
                # and don't just appear the same.
                if parent_ant is parent_ment:
                    # We allow for additional children
                    # according to the instance attributes.
                    if len(parent_ant) <= self.allowed_len:
                        appositive = True
                        for child in parent_ant:
                            is_ant = child is ant_tree
                            is_ment = child is ment_tree
                            is_allowed = child.label() in self.allowed_labels
                            if not (is_ant or is_ment or is_allowed):
                                appositive = False
                        if appositive:
                            return True
        return False
