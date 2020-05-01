#!/bin/env python
# -*- coding: utf-8 -*-

def print_upper_triangular_matrix(matrix):
    """prints a CVRP data dict matrix"""

    # print column header
    # Assumes first row contains all needed headers
    first = sorted(matrix.keys())[0]
    print( '\t',)
    for i in matrix[first]:
        print( '{}\t'.format(i),)
    print()

    indent_count = 0

    for i in matrix:
        # print line header
        print( '{}\t'.format(i),)

        if indent_count:
            print( '\t' * indent_count,)

        for j in sorted(matrix[i]): # required because dict doesn't guarantee insertion order
            print( '{}\t'.format(matrix[i][j]),)

        print()

        indent_count = indent_count + 1

def print_upper_triangular_matrix_as_complete(matrix):
    """prints a CVRP data dict upper triangular matrix as a normal matrix

    Doesn't print header"""
    for i in sorted(matrix.keys()):
        for j in sorted(matrix.keys()):
            a, b = i, j
            if a > b:
                a, b = b, a

            print( matrix[a][b],)

        print()

def print_solution(solution):
    """prints a solution

    Solution is an instance of project.solvers.BaseSolution

    Example:
        [8, 9, 10, 7]: 160
        [5, 6]: 131
        [3, 4, 2]: 154
        Total cost: 445
    """
    total_cost = 0
    for solution in solution.routes():
        cost = solution.length()
        total_cost = total_cost + cost
        print( '{}: {}'.format(solution, cost))
    print( 'Total cost: {}'.format(total_cost))
