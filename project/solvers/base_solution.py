#!/bin/env python
# -*- coding: utf-8 -*-

class BaseSolution(object):
    """Base abstract class for a CVRP solution"""

    def process(self, pair):
        """Processes a pair of nodes into the current solution

        Returns a new instance (deep copy) of self object
        """
        raise NotImplementedError()

    def can_process(self, pairs):
        """Returns True if this solution can process `pairs`

        Parameters:
            pairs: List of pairs
        """
        raise NotImplementedError()

    def routes(self):
        """Returns a generator for iterating over solution routes"""
        raise NotImplementedError()

    def length(self):
        """Returns the solution length (or cost)"""
        raise NotImplementedError()
