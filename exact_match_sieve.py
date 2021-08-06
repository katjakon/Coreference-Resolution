# -*- coding: utf-8 -*-
"""
A class that represents the exact sieve.
It gets clusters as input and links mentions if they are the same string.
"""


# TODO: Implement abstract class Sieve that has method resolve.
class ExactMatchSieve:

    def resolve(self, cluster):
        unresolved = cluster.unresolved()
        for mention in unresolved:
            # Sieve only operates on nominal mentions.
            if not mention.pronominal():
                same_ant, prev_ant = cluster.antecedents(mention)
                # Iterates first over antecedents from same,
                # then from previous sentence.
                all_antecedents = same_ant + prev_ant
                for mention_ant in all_antecedents:
                    if self.is_exact_match(mention_ant, mention):
                        cluster.merge(mention_ant, mention)
                        # mention is now assigned to a cluster, so we
                        # don't need to look any further.
                        break

    def is_exact_match(self, mention1, mention2):
        if mention1.words == mention2.words:
            return True
        return False
