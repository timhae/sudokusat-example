#!/usr/bin/env python3

import math
import subprocess
import argparse
import os


class Solver:
    def __init__(self):
        """Setup all internal variables"""

        parser = argparse.ArgumentParser(description='Create constraint files for sudoku solvers.')
        parser.add_argument('solver', help='The solver to use.')
        parser.add_argument('task', help='Filepath of the problem description to solve.')
        args = parser.parse_args()

        # basename of the task file w/o ending, will be used for intermediate filenames
        self.task = os.path.basename('.'.join(args.task.split('.')[0:-1]))
        # the specified solver
        self.solver = args.solver
        # internal representation of the sudoku, 2d array containing numbers, 0 for '_' in input
        self.sudoku = [[]]
        # cnf file content
        self.cnf = ''
        # task solution content
        self.solution = []
        # short problem description that will be included in the solution
        self.problem_description = ''
        # how many chars we need to print a number, depends on the size
        self.chars_per_number = 0
        # numbers per row/column
        self.size = 0
        # numbers per block
        self.small_size = 0

        self.solve()

    def solve(self):
        """Solve the given task"""

        # create the cnf out of the input
        self.read_sudoku()
        self.create_cnf()
        with open(self.task + '.cnf', 'w') as file_cnf:
            file_cnf.write('\n'.join(self.cnf))

        # solve the cnf with the given solver and store result in a file
        with open(self.task + '.sol', 'w') as file_solved:
            subprocess.run([self.solver, self.task + '.cnf'], stdout=file_solved)

        # create the solution with the help of the solver output
        self.read_solver_output()
        self.create_solution()
        with open(self.task + '_solution.txt', 'w') as file_solution:
            file_solution.write('\n'.join(self.solution))

    def read_sudoku(self):
        """Parse input file and create two-dimensional array for internal representation as well as problem description.

        INDEPENDENT OF ENCODING
        """

        # read file
        with open(self.task + '.txt') as file_input:
            entire_file = file_input.readlines()

        # get problem description in first 3 lines
        self.problem_description = [line.strip() for line in entire_file[0:4]]
        # get puzzle size, assume it is always in line 4
        self.size = int(entire_file[3].split()[2].split('x')[0])
        self.small_size = int(math.sqrt(self.size))
        self.chars_per_number = len(str(self.size))

        # select relevant lines (no divider lines)
        sudoku_lines = [line for (i, line) in enumerate(entire_file[4:]) if i % (self.small_size + 1) != 0]

        # create and fill array
        self.sudoku = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for (i, line) in enumerate(sudoku_lines):
            # filter '|' characters
            clean_line = [c for (i, c) in enumerate(line.split()) if i % (self.small_size + 1) != 0]
            for (j, number) in enumerate(clean_line):
                if '_' in number:
                    self.sudoku[i][j] = 0
                else:
                    self.sudoku[i][j] = int(number)

    def create_solution(self):
        """Parse sudoku array and return a printable representation with information from original task.

        INDEPENDENT OF ENCODING
        """

        # task information
        self.solution.append('\n'.join(self.problem_description))
        # fill solution string
        delimiter_row = self.small_size * ('+-' + ('-' * (self.small_size * (self.chars_per_number + 1)))) + '+'
        self.solution.append(delimiter_row)
        for line_number, line in enumerate(self.sudoku):
            linestring = '| '
            for column_number, column in enumerate(line):
                linestring += str(column).rjust(self.chars_per_number) + ' '
                if column_number % self.small_size == (self.small_size - 1):
                    linestring += '| '
            self.solution.append(linestring)
            if line_number % self.small_size == (self.small_size - 1):
                self.solution.append(delimiter_row)

    def read_solver_output(self):
        """Read solver output and create solved sudoku representation.

        SOLVER AND ENCODING DEPENDENT
        """

        with open(self.task + '.sol', 'r') as solver_output:
            solution = solver_output.readlines()

        # filter relevant elements
        relevant = []
        for line in solution:
            if line[0] == 'v':
                for elem in line.split()[1:]:
                    if elem > '110':
                        relevant.append(elem)

        # fill solution sudoku
        for elem in relevant:
            self.sudoku[int(elem[0]) - 1][int(elem[1]) - 1] = int(elem[2])

    def create_cnf(self):
        """Create cnf from internal sudoku representation.

        ENCODING DEPENDENT
        """
        # TODO: create cnf with the help of self.sudoku
        self.cnf = ['p cnf 2 2', '1 2 0', '-1 -2 0']


if __name__ == '__main__':
    Solver()
