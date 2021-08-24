# -*- coding: utf-8 -*-
"""
Coreference resolution
"""
from abstract_sieve import AbstractSieve
from clusters import Clusters

# TODO: Evaluation


class CoreferenceResolution:

    def __init__(self, doc, sieves):
        for sieve in sieves:
            if not isinstance(sieve, AbstractSieve):
                raise ValueError("Sieves must inherit from AbstractSieve")
        self.sieves = sieves
        self.doc = doc
        self.clusters = Clusters(self.doc)

    def resolve(self):
        for sieve in self.sieves:
            sieve.resolve(self.clusters)
