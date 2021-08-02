# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:28:07 2021

@author: HP I5
"""
import os
import re

from ontonotes_doc import OntonotesDoc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class OntonotesCorpus:

    FILE_EXT = "conll"

    def __init__(self, root, walk=False):
        self.root = os.path.join(ROOT, root)
        self.files = []
        self.index = 0

        f_suff = re.compile(r"[.].*" + self.FILE_EXT)
        for file in os.listdir(self.root):
            file_path = os.path.join(self.root, file)
            if os.path.isfile(file_path) and re.search(f_suff, file):
                self.files.append(file)

    def documents(self, file_ids=None):
        docs = []
        if file_ids is None:
            file_ids = self.files
        for file in file_ids:
            if file not in self.files:
                raise FileNotFoundError("Invalid file name: {}".format(file))
            doc = OntonotesDoc(file, os.path.join(self.root, file))
            docs.append(doc)
        return docs

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.files):
            file = OntonotesDoc(self.files[self.index], os.path.join(self.root, self.files[self.index]))
            self.index += 1
            return file
        else:
            self.index = 0
            raise StopIteration


if __name__ == "__main__":
    corpus = OntonotesCorpus("test")
    for doc in corpus:
        print(doc)
    print("-----")
    for doc in corpus:
        print(doc)
