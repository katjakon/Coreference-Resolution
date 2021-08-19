# -*- coding: utf-8 -*-
"""
A feature that determines if an antecedent and a mention
are in an predicate nominative construction
"""


class PredicateNominative:

    SENT = {"S", "SBAR"}
    VP = {"VP"}

    def __init__(self, predicate=("be",)):
        self.predicate = predicate

    def has_feature(self, cluster, antecedent, mention):
        # Get the sentence object that contains the mention
        sentence = cluster.sentence(mention)
        if antecedent.index() == mention.index():
            # The mention should be in the VP (object)
            ment_parent = self._get_parent(mention, self.VP)
            # The antecedent should be the subject, so its parent
            # should be an S/SBAR node
            ant_parent = self._get_parent(antecedent, self.SENT)
            if ment_parent is not None and ant_parent is not None:
                # Making sure the VP that contains the mention,
                # is the VP of the S/SBAR tree of the antecedent.
                if ment_parent.parent() is ant_parent:
                    # TODO: Make sure VP is predicate
                    pass

    def _get_parent(self, mention, parent_label):
        parent = mention.tree.parent()
        if parent is None or parent.label() not in parent_label:
            return None
        return parent
