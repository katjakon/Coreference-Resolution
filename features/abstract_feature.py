# -*- coding: utf-8 -*-
"""
Abstract Class for Features
"""
from abc import ABC, abstractmethod


class AbstractClusterFeature(ABC):

    @abstractmethod
    def has_feature():
        """This method determines if the concrete feature applies
        to two clusters of mentions. It should return a Boolean value and
        take a cluster and two mentions as input.
        """
        pass


class AbstractMentionFeature(ABC):

    @abstractmethod
    def has_feature():
        """This method also determines if a feature applies but
        it should only take two mentions as input. It should return
        a Boolean Value"""
        pass
