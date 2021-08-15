# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 13:28:59 2021

@author: HP I5
"""
from nltk.tree import Tree, ParentedTree


class IndexedTree(ParentedTree):

    def __init__(self, label, children=None, delimiter="_", index=False):
        super().__init__(label, children)
        leaves = self.leaves()
        if index:
            for leaf in leaves:
                leaf = leaf.split(delimiter)
                if len(leaf) != 2:
                    raise Exception
                if not leaf[1].isdecimal():
                    raise Exception
        self.delimiter = delimiter
        self.indexed = index

    def index(self):
        if not self.indexed:
            leaf_pos = self.treepositions("leaves")
            for idx, leaf in enumerate(leaf_pos):
                self[leaf] = f"{self[leaf]}{self.delimiter}{idx}"
        self.indexed = True

    def _token(self, string):
        return string.split(self.delimiter)[0]

    def _index(self, string):
        if self.indexed:
            return int(string.split(self.delimiter)[1])
        raise Exception

    def span(self):
        if self.indexed:
            leaves = self.leaves()
            start = self._index(leaves[0])
            end = self._index(leaves[-1]) + 1
            return start, end
        raise Exception

    def leaves(self, indexed=True):
        leaves = super().leaves()
        if indexed:
            return leaves
        return [self._token(leaf) for leaf in leaves]

    def pos(self):
        pos = super().pos()
        return [(self._token(tok), p) for tok, p in pos]



t = "(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))"
tree = Tree.fromstring(t)
it = IndexedTree.convert(tree)
it.index()

for i in it.subtrees():
    print(type(i))

