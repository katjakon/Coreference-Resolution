# -*- coding: utf-8 -*-
"""
A feature that determines if an antecedent and a mention
are in an predicate nominative construction
"""
from nltk.tree import Tree


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
                    verb = self._get_verb(ment_parent)
                    if verb:
                        # Leaves are tuples of token and index.
                        _, index = verb
                        # Check if extracted verb is a predicate.
                        lemma = sentence.lemma()
                        if lemma[int(index)] in self.predicate:
                            return True
        return False

    def _get_verb(self, vp):
        # Base case: reached a leaf.
        if not isinstance(vp, Tree):
            return vp
        n_verbs = 0
        index_verb = 0
        for idx, child in enumerate(vp):
            # There should be only one verb in the VP.
            if n_verbs > 1:
                return None
            if isinstance(child, Tree) and child.label().startswith("V"):
                index_verb = idx
                n_verbs += 1
        return self._get_verb(vp[index_verb])

    def _get_parent(self, mention, parent_label):
        parent = mention.tree.parent()
        if parent is None or parent.label() not in parent_label:
            return None
        return parent
