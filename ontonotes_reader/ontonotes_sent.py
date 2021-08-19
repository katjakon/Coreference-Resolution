# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:47:36 2021

@author: HP I5
"""
from ontonotes_reader.indexed_tree import IndexedTree
from nltk.tree import Tree


class OntonotesSent:

    WORD_ID_COL = 2
    WORD_COL = 3
    POS_COL = 4
    TREE_COL = 5
    NE_COL = 10
    COREF_COL = -1
    DELIMITER = "_"

    def __init__(self, sent_id, conll_sentence):
        self._id = sent_id
        self._words = []
        self._tree = None
        self._pos = []
        self._ne = dict()
        self._coref = dict()

        self.process_conll(conll_sentence)

    def process_conll(self, conll_sentence):
        tree_str = ""
        coref_stack = dict()
        ne_stack = []
        for line in conll_sentence:
            word = line[self.WORD_COL]
            pos = line[self.POS_COL]
            word_id = int(line[self.WORD_ID_COL])
            self._words.append(word)
            self._pos.append(pos)
            word_pos = f"({pos} {word})"
            tree_str += line[self.TREE_COL].replace("*", word_pos)
            # Read coreference information.
            coref = line[self.COREF_COL]
            if not coref.startswith("-"):
                coref_split = coref.split("|")
                for coref in coref_split:
                    coref_id = int(coref.strip("(").strip(")"))
                    if coref.startswith("("):
                        coref_stack.setdefault(coref_id, [])
                        coref_stack[coref_id].append(word_id)
                    if coref.endswith(")"):
                        start = coref_stack[coref_id].pop()
                        self._coref.setdefault(coref_id, [])
                        self._coref[coref_id].append((start, word_id+1))
            # Read named entity information.
            ne = line[self.NE_COL]
            if not ne.startswith("*"):
                ne = ne.strip("(").strip(")")
                if not ne.endswith("*"):
                    self._ne.setdefault(ne, [])
                    self._ne[ne].append((word_id, word_id+1))
                else:
                    ne = ne.strip("*")
                    ne_stack.append((ne, word_id))
            else:
                if ne.endswith(")"):
                    ne_type, start = ne_stack.pop()
                    self._ne.setdefault(ne_type, [])
                    self._ne[ne_type].append((start, word_id+1))
        # Some tree strings from ontonotes seem to be malformed
        try:
            self._tree = IndexedTree.fromstring(tree_str)
            # Indexing the tree helps
            # to identify spanning subtrees.
            self._tree.index()
        except ValueError as e:
            print(f"IGNORED {self._id}")

    def named_entities(self):
        return self.ne

    def coreference(self):
        return self._coref

    def tree(self):
        return self._tree

    def words(self, tagged=True):
        if tagged:
            return list(zip(self._words, self._pos))
        return self._words

    @property
    def index(self):
        return self._id

    def __getitem__(self, index):
        return self._words[index]
