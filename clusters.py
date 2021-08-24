# -*- coding: utf-8 -*-
"""
A class that represents clusters in a document.
Clusters are essentially a disjoint-set structure.
"""
from collections import deque

from nltk.tree import Tree

from mention import Mention


class Clusters:

    RE = {"NP", "PRP$"}

    def __init__(self, doc):
        self._doc = doc
        self.clusters = dict()
        self.mentions = dict()

        self._intialize()

    def _intialize(self):
        for sentence in self._doc:
            tree = sentence.tree()
            for subt in tree.subtrees(filter=lambda t: t.label() in self.RE):
                start, end = subt.span()
                mention_id = (sentence.index, start, end)
                mention = Mention(mention_id, subt)
                self.clusters[mention] = {mention}
                self.mentions[mention_id] = mention

    def sentence(self, mention):
        return self._doc[mention.index()]

    def find(self, mention):
        return mention.pointer

    def merge(self, first, second):
        repr_first = self.find(first)
        repr_second = self.find(second)
        # Both mentions are already in the same cluster.
        if repr_first == repr_second:
            return False
        # Perfom union of mentions and delete second (later) cluster.
        second_mentions = self.clusters.pop(repr_second)
        first_mentions = self.clusters[repr_first]
        self.clusters[repr_first] = first_mentions.union(second_mentions)
        # Set new pointers for all mentions in second cluster
        for mention in second_mentions:
            mention.pointer = repr_first
        return True

    def antecedents(self, mention):
        # We have seen this mention before and extracted its antecedents.
        if mention.antecedents:
            return mention.antecedents
        index, start, end = mention.id
        prev = index - 1
        # Get mentions in previous sentence
        prev_sent = []
        if prev >= 0:
            prev_tree = self._doc[prev].tree()
            # If a mention is pronominal, we search left to right,
            # otherwise we search right to left.
            prev_sent = self._bfs(prev_tree, left_to_right=mention.pronominal)
        # Get mentions in same sentence
        tree = self._doc[index].tree()
        same_sent = self._bfs(tree, mention=mention)
        # Get the mention objects from the mention id.
        same_sent_id = [self.mentions[(index, start, end)]
                        for start, end in same_sent]
        prev_sent_id = [self.mentions[(prev, start, end)]
                        for start, end in prev_sent]
        # Set antecedents for mention to avoid unnecessary computations.
        antecedents = same_sent_id + prev_sent_id
        mention.antecedents = antecedents
        return antecedents

    def _bfs(self, tree, left_to_right=True, mention=None):
        queue = deque()
        queue.append(tree)
        while queue:
            next_tree = queue.popleft()
            if next_tree.label() in self.RE:
                span = next_tree.span()
                if mention:
                    # If this is the case we have reached the mention,
                    # and don't need to look for more antecedents.
                    if span == mention.span():
                        return
                yield span
            if not left_to_right:
                next_tree = reversed(next_tree)
            for child in next_tree:
                if isinstance(child, Tree):
                    queue.append(child)

    def unresolved(self):
        # Mentions are sorted by sentence index first,
        # start and end index second.
        return sorted(self.clusters.keys(), key=lambda m: m.id)

    def __str__(self):
        string = f"<ClustersObject with {len(self.clusters)} Clusters>\n"
        for mention in self.clusters:
            string += f"{mention}:\t{self.clusters[mention]}\n"
        return string

    def __getitem__(self, mention):
        if isinstance(mention, tuple):
            mention = self.mentions[mention]
        repr_ment = self.find(mention)
        return self.clusters[repr_ment]
