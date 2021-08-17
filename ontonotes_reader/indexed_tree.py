# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 13:28:59 2021

@author: HP I5
"""
from nltk.tree import Tree, ParentedTree


class IndexedTree(ParentedTree):

    def __init__(self, label, children=None, delimiter="_"):
        super().__init__(label, children)
        self.indexed = False

    def index(self):
        if not self.indexed:
            leaf_pos = self.treepositions("leaves")
            for idx, leaf in enumerate(leaf_pos):
                # str(idx) is used because,
                # print methods won't work otherwise.
                self[leaf] = (self[leaf], str(idx))
            self._set_indexed()

    def _set_indexed(self):
        self.indexed = True
        for child in self:
            if isinstance(child, IndexedTree):
                child._set_indexed()

    def _token(self, leaf):
        return leaf[0]

    def _index(self, leaf):
        return int(leaf[1])

    def span(self):
        if self.indexed:
            leaves = self.leaves(True)
            start = self._index(leaves[0])
            end = self._index(leaves[-1]) + 1
            return start, end
        raise Exception

    def leaves(self, indexed=False):
        leaves = []
        for child in self:
            if isinstance(child, IndexedTree):
                leaves.extend(child.leaves(indexed))
            else:
                if indexed:
                    leaves.append(child)
                else:
                    leaves.append(self._token(child))
        return leaves

    def pos(self):
        pos = super().pos()
        return [(self._token(tok), p) for tok, p in pos]
