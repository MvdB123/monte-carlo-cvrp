#!/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import sys

from project.solvers import sequential_clarke_wright

class BinaryMCSCWSSolution(sequential_clarke_wright.SequentialClarkeWrightSolution):
    """Solution class for a BinaryMCS-CWS algorithm"""

class BinaryMCSCWSSolver(sequential_clarke_wright.SequentialClarkeWrightSolver):
    """BinaryMCS-CWS algorithm solver class"""

    def __init__(self):
        self._best = None

    def simulation(self, solution, pair, savings_list):
        """Do a Monte Carlo Simulation"""
        for i, j in savings_list:
            if solution.can_process((i, j)):
                if random.random() > 0.1:
                    solution, inserted = solution.process((i, j))

        if self._best is None:
            self._best = solution
        elif (solution.length() < self._best.length()):
            self._best = solution

        return solution.length()

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using BinaryMCS-CWS method

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (BinaryMCSCWSSolution class))
        """
        start = time.time()
        savings_list = self.compute_savings_list(data)

        solution = BinaryMCSCWSSolution(data, vehicles)
        self._best = None

        savings_copy = savings_list[:]

        for i, j in savings_list:
            if solution.can_process((i, j)):
                processed, inserted = solution.process((i, j))

                if not inserted:
                    continue

                yes = 0
                no = 0

                for r in range(50): # simulations
                    yes = yes + self.simulation(processed.clone(), (i, j), savings_copy)
                    no = no + self.simulation(solution.clone(), (i, j), savings_copy)

                    if time.time() - start > timeout:
                        break

                if yes <= no:
                    solution = processed

            if time.time() - start > timeout:
                break

        if self._best is None:
            self._best = solution
        elif solution.length() < self._best.length():
            self._best = solution

        return self._best
