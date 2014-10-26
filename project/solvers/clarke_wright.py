#!/bin/env python
# -*- coding: utf-8 -*-

import operator
import time

from project.solvers.base import BaseSolution, BaseSolver

class ClarkeWrightSolution(BaseSolution):
    """Solution class for a Clarke and Wright Savings algorithm"""

    def process(self, pair):
        """Processes a pair of nodes into the current solution

        MUST CREATE A NEW INSTANCE, NOT CHANGE ANY INSTANCE ATTRIBUTES

        Returns a new instance (deep copy) of self object
        """
        a, b = pair

        new_solution = self.clone()

        i, j = new_solution.get_pair((a, b))

        inserted = False

        if i.route_allocation() is None and j.route_allocation() is None:
            # Try to add the two nodes to a route
            for route in new_solution._routes:
                if route.can_allocate([i, j]):
                    route.allocate([i, j])
                    new_solution._allocated = new_solution._allocated + 2
                    inserted = True
                    break
        # either i or j is allocated
        elif ((i.route_allocation() is not None and j.route_allocation() is None) or
                (j.route_allocation() is not None and i.route_allocation() is None)):
            inserted = None
            to_insert = None

            if i.route_allocation() is not None:
                inserted = i
                to_insert = j
            else:
                inserted = j
                to_insert = i

            route = inserted.route_allocation()

            # inserted not interior
            if not route.is_interior(inserted):
                if route.can_allocate([to_insert]):
                    append = False

                    if route.last(inserted):
                        append = True

                    route.allocate([to_insert], append)
                    new_solution._allocated = new_solution._allocated + 1
                    inserted = True

        return new_solution, inserted

    def can_process(self, pairs):
        """Returns True if this solution can process `pairs`

        Parameters:
            pairs: List of pairs
        """
        i, j = pairs

        # Neither points are in a route
        if i.route_allocation() is None or j.route_allocation() is None:
            return True

        if self._allocated == len(list(self._problem.nodes())) - 1: # All nodes in a route
            return False

        return False

class ClarkeWrightSolver(BaseSolver):
    """Clark and Wright Savings algorithm solver class"""
    def compute_savings_list(self, data):
        """Compute Clarke and Wright savings list

        A saving list is a matrix containing the saving amount S between i and j

        S is calculated by S = d(0,i) + d(0,j) - d(i,j) (CLARKE; WRIGHT, 1964)
        """

        savings_list = {}

        for i, j in data.edges():
            t = (i, j)

            if i == data.depot() or j == data.depot():
                continue

            savings_list[t] = data.distance(data.depot(), i) + data.distance(data.depot(), j) - data.distance(i, j)

        sorted_savings_list = sorted(savings_list.items(), key=operator.itemgetter(1), reverse=True)

        return [nodes for nodes, saving in sorted_savings_list]

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using Clarke and Wright Savings methods

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (ClarkeWrightSolution class))
        """
        savings_list = self.compute_savings_list(data)

        solution = ClarkeWrightSolution(data, vehicles)

        start = time.time()

        for i, j in savings_list:
            if solution.can_process((i, j)):
                solution, inserted = solution.process((i, j))

            if time.time() - start > timeout:
                break

        return solution
