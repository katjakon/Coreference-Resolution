# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:45:58 2021

@author: HP I5
"""
import os

from .ontonotes_sent import OntonotesSent


class OntonotesDoc:

    def __init__(self, doc_id, path):
        self._id = doc_id
        self.path = path
        self._sentences = self._read_sentences()

    def _read_sentences(self):
        sentences = []
        tmp_sentence = []
        sent_id = 0
        with open(os.path.join(self.path), encoding="utf-8") as doc_file:
            for line in doc_file:
                if line.startswith("#"):
                    continue
                line = line.rstrip()
                if not line:
                    sentence = OntonotesSent(sent_id, tmp_sentence)
                    sentences.append(sentence)
                    sent_id += 1
                    tmp_sentence = []
                else:
                    tmp_sentence.append(line.split())
            if tmp_sentence:
                sentence = OntonotesSent(sent_id, tmp_sentence)
                sentences.append(sentence)
        return sentences

    def coreference_chains(self):
        coref_dict = dict()
        for sentence in self._sentences:
            sent_coref = sentence.coreference()
            for coref in sent_coref:
                coref_dict.setdefault(coref, {})
                coref_dict[coref][sentence.index] = sent_coref[coref]
        return coref_dict

    def named_entities(self):
        ne_dict = dict()
        for sent in self._sentences:
            ne_dict[sent.index] = sent._ne
        return ne_dict

    def __getitem__(self, index):
        return self._sentences[index]

    def __iter__(self):
        return iter(self._sentences)
