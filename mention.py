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
    INDEFINTIE = {"a", "an", "some", "no", "most", "any", "few", "many", "several", "there"}

    def __init__(self, mention_id, tree):
        self.id = mention_id
        self.pointer = self
        self.tree = tree

    @property
    def words(self):
        return self.tree.leaves()

    @property
    def pos(self):
        return self.tree.pos()

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

    def indefinite(self, tree=None):
        if tree is None:
            tree = self.tree
        # If there is a determiner, it is most likely in the first
        # constituent.
        first = tree[0]
        if not isinstance(first, Tree):
            if first[0].lower() in self.INDEFINTIE:
                return True
            # Obviously, this is a very relaxed heuristic,
            # e.g. bare NPs will always be interpreted as definite.
            else:
                return False
        return self.indefinite(first)

    def head(self, tree=None):
        if tree is None:
            tree = self.tree
        # Base case: tree is a leaf.
        if not isinstance(tree, Tree):
            # Leaves are tuples of (token, index)
            return tree[0]
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
