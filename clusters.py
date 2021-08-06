# -*- coding: utf-8 -*-
"""
A class that represents clusters in a document.
Clusters are essentially a disjoint-set structure.
"""

from nltk.tree import Tree

from mention import Mention


class Clusters:

    DELIMITER = "_"
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
                start, end = self._get_leaves_span(subt)
                mention_id = (sentence.index, start, end)
                mention = Mention(mention_id,
                                  subt,
                                  self._doc[sentence.index][start:end])
                self.clusters[mention] = {mention}
                self.mentions[mention_id] = mention

    # TODO: Determine if this methods is necessary.
    def words(self, mention):
        return mention.words

    def sentence_tree(self, mention):
        sentence_index = mention.id[0]
        return self._doc[sentence_index].tree()

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
        self.clusters[repr_first] = self.clusters[repr_first].union(second_mentions)
        # Set new pointers for all mentions in second cluster
        for m in second_mentions:
            m.pointer = repr_first
        return True

    # Get all possible antecdents sorted
    def antecedents(self, mention):
        index, start, end = mention.id
        prev = index - 1
        # Get mentions in previous sentence
        prev_sent_id = []
        is_pronominal = mention.pronominal()
        if prev >= 0:
            prev_tree = self._doc[prev].tree()
            # If a mention is pronominal, we search left to right,
            # otherwise we search right to left.
            prev_sent = self.bfs(prev_tree, left_to_right=is_pronominal)
            prev_sent_id = [self.mentions[(prev, start, end)]
                            for start, end in prev_sent]
        # Get mentions in same sentence
        tree = self._doc[index].tree()
        same_sent = self.bfs(tree, mention_id=mention.id)
        same_sent_id = [self.mentions[(index, start, end)]
                        for start, end in same_sent]
        return same_sent_id, prev_sent_id

    # TODO: What if tree is not indexed?
    def _get_leaves_span(self, tree):
        leaves = tree.leaves()
        start = int(leaves[0].split(self.DELIMITER)[-1])
        end = int(leaves[-1].split(self.DELIMITER)[-1]) + 1
        return start, end

    # TODO: Make this a generator instead of a function
    def bfs(self, tree, left_to_right=True, mention_id=None):
        queue = []
        spans = []
        queue.append(tree)
        while queue:
            next_tree = queue.pop(0)
            if next_tree.label() in self.RE:
                span = self._get_leaves_span(next_tree)
                # When we get to mention_id,
                # all possible antecendens have been found.
                if mention_id:
                    if span == mention_id[1:]:
                        break
                spans.append(span)
            children = [child for child in next_tree]
            if not left_to_right:
                children.reverse()
            for child in children:
                if isinstance(child, Tree):
                    queue.append(child)
        return spans

    def unresolved(self):
        unresolved = list(self.clusters.keys())
        # Mentions are sorted by sentence index first,
        # start and end index second.
        return sorted(unresolved, key=lambda m: m.id)

    def __str__(self):
        string = f"<ClustersObject with {len(self.clusters)} Clusters>\n"
        for mention in self.clusters:
            string += f"{mention}:\t{self.clusters[mention]}\n"
        return string

    def __getitem__(self, mention):
        return self.clusters[mention]

    def __iter__(self):
        clusters = ((first, self.clusters[first]) for first in self.clusters)
        return iter(clusters)

    def __next__(self):
        return next(iter(self))
