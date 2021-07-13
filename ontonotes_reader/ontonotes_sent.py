# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:47:36 2021

@author: HP I5
"""
from nltk.tree import Tree


class OntonotesSent:

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
        coref_stack = {}
        for line in conll_sentence:
            word = line[3]
            pos = line[4]
            word_id = int(line[2])
            self._words.append(word)
            self._pos.append(pos)
            word_pos = f"({pos} {word})"
            tree_str += line[5].replace("*", word_pos)
            coref = line[-1]
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
        self._tree = Tree.fromstring(tree_str)

    def words(self, tagged=True):
        if tagged:
            return list(zip(self._words, self._pos))
        return self._words

    def __getitem__(self, index):
        return self._words[index]
