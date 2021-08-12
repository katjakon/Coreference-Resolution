# -*- coding: utf-8 -*-
"""
An abstract class for sieves.
"""

from abc import ABC, abstractmethod


class AbstractSieve(ABC):

    @abstractmethod
    def resolve():
        """This method should recieve a Cluster object as input
        and perform some merging operations on the mentions in the cluster.
        """
        pass
