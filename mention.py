# -*- coding: utf-8 -*-
"""
Class that represents a mention aka a referential expression.
A mention is definded by a unique id consisting of (sentence_index, start, end)
"""
import re

from nltk.tree import Tree


class Mention:

    PRONOUNS = {"PRP", "DT", "PRP$"}
    NOMINAL = re.compile(r"NN?P?S?")
    INDEFINTIE = {"a",
                  "an",
                  "some",
                  "no",
                  "most",
                  "any",
                  "few",
                  "many",
                  "several",
                  "there"}

    def __init__(self, mention_id, tree):
        self.id = mention_id
        self.pointer = self
        self.tree = tree
        self.antecedents = None
        self._pronominal = self._is_pronominal(self.tree)
        self._indefinite = self._is_indefinite(self.tree)
        self._head = self._get_head(self.tree)
        self._words = self.tree.leaves()
        self._pos = self.tree.pos()

    @property
    def words(self):
        return self._words

    @property
    def pos(self):
        return self._pos

    @property
    def pronominal(self):
        return self._pronominal

    @property
    def indefinite(self):
        return self._indefinite

    @property
    def head(self):
        return self._head

    def span(self):
        return self.id[1], self.id[2]

    def index(self):
        return self.id[0]

    def _is_pronominal(self, tree):
        # A pronoun is contained in a tree where each
        # node has exactly one child.
        if len(tree) == 1:
            child = tree[0]
            # Accounts for cases like: (PRP$ his)
            if tree.label() in self.PRONOUNS:
                return True
            # Accounts for cases like: (NP (PRP he))
            elif isinstance(child, Tree):
                # This is recursive because pronouns can have structure:
                # (NP (NP (PRP it)))
                return self._is_pronominal(child)
        return False

    def _is_indefinite(self, tree):
        # Base case: Reached a leaf.
        if not isinstance(tree, Tree):
            # Leaf token is an indefinite determiner.
            if tree[0].lower() in self.INDEFINTIE:
                return True
            # Obviously, this is a very relaxed heuristic,
            # e.g. bare NPs will always be interpreted as definite.
            else:
                return False
        # If there is a determiner, it is most likely in the first
        # constituent.
        return self._is_indefinite(tree[0])

    def _get_head(self, tree):
        # Base case: tree is a leaf.
        if not isinstance(tree, Tree):
            # Leaves are tuples of (token, index)
            return tree[0]
        # Because of right headedness, we search for the first
        # nominal constituent from right to left in all children.
        for i in range(len(tree)-1, -1, -1):
            child = tree[i]
            if isinstance(child, Tree) and self.NOMINAL.search(child.label()):
                return self._get_head(child)
        # This is a fall back: As english has right headedness in nouns,
        # the naive approach is to assume the last child contains the head.
        return self._get_head(tree[-1])

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other

    def __repr__(self):
        return f"Mention{self.id}"

    def __str__(self):
        words = " ".join(self.words)
        return f"<Mention{self.id}, '{words}'>"
