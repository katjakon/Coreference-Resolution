# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:45:58 2021

@author: HP I5
"""
import os

from ontonotes_sent import OntonotesSent


class OntonotesDoc:

    def __init__(self, doc_id, path):
        self._id = doc_id
        self.path = path
        self._sentences = self.read_sentences()

    def read_sentences(self):
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
        return sentences

    def coreference_chains(self):
        coref_dict = dict()
        chains = dict()
        for sentence in self._sentences:
            for coref in sentence._coref:
                coref_dict.setdefault(coref, {})
                coref_dict[coref].setdefault(sentence._id, [])
                coref_dict[coref][sentence._id].extend(sentence._coref[coref])
        # for coref in coref_dict:
        #     for sent_id in coref_dict[coref]:
        #         for start, end in coref_dict[coref][sent_id]:
        #             chains.setdefault(coref, [])
        #             chains[coref].append(self[sent_id][start:end])
        return coref_dict

    def named_entities(self):
        ne_dict = dict()
        for sent in self._sentences:
            ne_dict[sent._id] = sent._ne
        return ne_dict

    def __getitem__(self, index):
        return self._sentences[index]


if __name__ == "__main__":
    f = "bc_cctv_0002.v4_auto_conll"
    doc = OntonotesDoc(0, f)
    ne = doc.named_entities()
    print(ne)
