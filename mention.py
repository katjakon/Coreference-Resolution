# -*- coding: utf-8 -*-
"""
Class that represents a mention aka a referential expression.
A mention is definded by a unique id consisting of (sentence_index, start, end)
"""
import re

from nltk.tree import Tree


# TODO: Some features are computed repeatedly, even though they don't change.
class Mention:

    PRONOUNS = {"PRP", "DT", "PRP$"}
    NOMINAL = re.compile(r"NN?P?S?")
    INDEFINTIE = {"a", "an", "some", "no", "most", "any", "few", "many", "several"}

    def __init__(self, mention_id, tree, words):
        self.id = mention_id
        self.pointer = self
        self.tree = tree
        self.words = words

    def pronominal(self, tree=None):
        if tree is None:
            tree = self.tree
        if len(tree) == 1:
            child = tree[0]
            # Accounts for cases like: (PRP$ his)
            if tree.label() in self.PRONOUNS:
                return True
            # Accounts for cases like: (NP (PRP he))
            elif isinstance(child, Tree):
                # This is recursive because pronouns can have structure:
                # (NP (NP (PRP it)))
                return self.pronominal(child)
        return False

    # TODO: Determine if a mention is indefinite or not.
    def indefinite(self):
        first = self.tree.leaves()[0]
        if first in self.INDEFINTIE:
            return True
        return False

    # TODO: Deal with Coordination.
    def head(self, tree=None):
        if tree is None:
            tree = self.tree
        # Base case: tree is pre-terminal.
        if len(tree) == 1 and not isinstance(tree[0], Tree):
            return tree.leaves()[0]
        # Because of right headedness, we search for the first
        # nominal constituent from right to left in all children.
        for i in range(len(tree)-1, -1, -1):
            child = tree[i]
            if isinstance(child, Tree) and self.NOMINAL.search(child.label()):
                return self.head(child)
        # This is a fall back: As english has right headedness in nouns,
        # the naive approach is to assume the last child contains the head.
        return self.head(tree[-1])

    def span(self):
        return self.id[1], self.id[2]

    def index(self):
        return self.id[0]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other

    def __repr__(self):
        return f"Mention{self.id}"

    def __str__(self):
        words = " ".join(self.words)
        return f"<Mention{self.id}, '{words}'>"
