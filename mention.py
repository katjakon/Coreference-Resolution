# -*- coding: utf-8 -*-
"""
Class that represents a mention aka a referential expression.
A mention is definded by a unique id consisting of (sentence_index, start, end)
"""
from nltk.tree import Tree


class Mention:

    PRONOUNS = {"PRP", "DT", "PRP$"}

    def __init__(self, mention_id, tree, words):
        self.id = mention_id
        self.pointer = self
        self.tree = tree
        self.words = words

    def pronominal(self):
        if len(self.tree) == 1:
            child = self.tree[0]
            # Accounts for cases like: (NP (PRP he))
            if isinstance(child, Tree) and child.label() in self.PRONOUNS:
                return True
            # Accounts for cases like: (PRP$ his)
            elif self.tree.label() in self.PRONOUNS:
                return True
        return False

    # TODO: Determine if a mention is indefinite or not.
    def indefinite(self):
        pass

    # TODO: Determine the head noun of a mention.
    def head(self):
        pass

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
