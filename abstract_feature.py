# -*- coding: utf-8 -*-
"""
Abstract Class for Features
"""
from abc import ABC, abstractmethod


class AbstractFeature(ABC):

    @abstractmethod
    def has_feature():
        """This method determines if the concrete feature applies
        to two mentions. It should return a Boolean value."""
        pass
