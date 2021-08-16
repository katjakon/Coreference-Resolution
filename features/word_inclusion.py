# -*- coding: utf-8 -*-
"""
A class that represents the word inclusion feature
"""
from nltk.corpus import stopwords

from features.abstract_feature import AbstractClusterFeature


class WordInclusion(AbstractClusterFeature):

    def __init__(self, lang="english"):
        if lang not in stopwords.fileids():
            raise NotImplementedError(f"Unknown language: {lang}")
        self.stopwords = stopwords.words(lang)

    def has_feature(self, clusters, antecedent, mention):
        non_stops_ment = self._get_non_stopwords(clusters[mention])
        non_stops_ant = self._get_non_stopwords(clusters[antecedent])
        if non_stops_ment.issubset(non_stops_ant):
            return True
        return False

    def _get_non_stopwords(self, cluster):
        non_stops = set()
        for mention in cluster:
            for word in mention.words:
                if word not in self.stopwords:
                    non_stops.add(word)
        return non_stops
