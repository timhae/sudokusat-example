#!/usr/bin/env python3

import signal
import math
import subprocess
import argparse
import os


class Solver:
    def __init__(self):
        """Create all internal variables, they will be set up later."""

        # setup interrupt handling
        signal.signal(signal.SIGTERM, self.handler)
        signal.signal(signal.SIGINT, self.handler)

        # parse arguments
        parser = argparse.ArgumentParser(description='Create constraint files for sudoku solvers.')
        parser.add_argument('solver', help='The solver to use.')
        parser.add_argument('task', help='Filepath of the problem description to solve.')
        args = parser.parse_args()

        # problem instance path
        self.problem = '.'.join(args.task.split('.')[0:-1])
        # basename of the task file w/o ending, will be used for intermediate filenames
        self.task = os.path.basename(self.problem)
        # the specified solver
        self.solver = args.solver
        # internal representation of the sudoku, 2d array containing tuples with the current entry and
        # a set with all possible values for that cell
        self.sudoku = [[]]
        # short problem description that will be included in the solution
        self.problem_description = []
        # how many chars we need to print a number, depends on the size
        self.chars_per_number = 0
        # total lines/columns, big sudoku size, n^2=9 for n=3
        self.size = 0
        # lines per block, small sudoku size, n
        self.small_size = 0
        # large sudoku range list [0, .., 8] for n=3 sudoku (9 elements)
        self.rlb = []
        # large sudoku range list shifted [1, .., 9] for n=3 sudoku (9 elements)
        self.rlb_shifted = []
        # small sudoku range list [0, .., 2] for n=3 sudoku (3 elements)
        self.rls = []
        # small sudoku range list shifted [1, .., 3] for n=3 sudoku (3 elements)
        self.rls_shifted = []
        # commander encoding var group size
        self.cmdr_size = 5
        # cnf variable counter
        self.num_vars = 0
        # the clasp process
        self.process = None

        self.solve()

    def handler(self, _num, _frame):
        if self.process is not None:
            self.process.terminate()

    def solve(self):
        """Solve the given task."""

        # create the cnf out of the input
        self.read_sudoku()
        self.create_cnf()

        # solve the cnf with the given solver and store result in a file
        with open(self.task + '.sol', 'w') as file_solved:
            self.process = subprocess.Popen([self.solver, self.task + '.cnf'], stdout=file_solved)
        self.process.wait()

        # create the solution with the help of the solver output
        self.read_solver_output()
        self.create_solution()

    def read_sudoku(self):
        """Parse input file and create two-dimensional array for internal representation as well as problem description.

        INDEPENDENT OF ENCODING
        """

        # read file
        with open(self.problem + '.txt') as file_input:
            entire_file = file_input.readlines()

        # get problem description in first 3 lines
        self.problem_description = [line.strip() for line in entire_file[0:4]]
        # get puzzle size, assume it is always in line 4
        self.size = int(entire_file[3].split()[2].split('x')[0])
        self.small_size = int(math.sqrt(self.size))
        self.chars_per_number = len(str(self.size))
        self.num_vars = int(''.join([str(self.size) for _ in range(3)]))

        # select relevant lines (no divider lines)
        sudoku_lines = [line for (i, line) in enumerate(entire_file[4:]) if i % (self.small_size + 1) != 0]

        # create and fill array
        self.rlb = list(range(self.size))  # range list big
        self.rlb_shifted = self.rlb[1:] + [self.size]  # shifted
        self.rls = list(range(self.small_size))  # range list small
        self.rls_shifted = self.rls[1:] + [self.small_size]  # shifted
        self.sudoku = [[[
            0, set(([temp for temp in self.rlb_shifted]))]
            for _ in self.rlb]
            for _ in self.rlb]
        for (i, line) in enumerate(sudoku_lines):
            # filter '|' characters
            clean_line = [c for (temp, c) in enumerate(line.split()) if temp % (self.small_size + 1) != 0]
            for (j, number) in enumerate(clean_line):
                if '_' in number:
                    self.sudoku[i][j][0] = 0
                else:
                    self.set_number_and_eliminate(int(number), i, j)

    def create_cnf(self):
        """Create cnf from internal sudoku representation.

        ENCODING DEPENDENT
        """

        clauses = []  # List to maintain all the clauses

        def vals_to_clause(n1, n2, n3):
            """Prepend resulting clause string with 0 if necessary."""
            # TODO: fix encoding for n>9
            string = str(n1)\
                + str(n2).zfill(self.chars_per_number)\
                + str(n3).zfill(self.chars_per_number)
            return string

        # cell definedness
        for rows in self.rlb_shifted:
            for cols in self.rlb_shifted:
                clause = ''
                for value in self.rlb_shifted:
                    clause += vals_to_clause(rows, cols, value) + ' '
                clause += str(0)
                clauses.append(clause)

        # row uniqueness
        for rows in self.rlb_shifted:
            for value in self.rlb_shifted:
                for x in range(1, self.size):
                    for y in range(x + 1, self.size + 1):
                        clauses.append('-' + vals_to_clause(rows, x, value) +
                                       ' -' + vals_to_clause(rows, y, value) + ' 0')

        # column uniqueness
        for cols in self.rlb_shifted:
            for value in self.rlb_shifted:
                for x in range(1, self.size):
                    for y in range(x + 1, self.size + 1):
                        clauses.append('-' + vals_to_clause(x, cols, value) +
                                       ' -' + vals_to_clause(y, cols, value) + ' 0')

        # block uniqueness
        for value in self.rlb_shifted:
            for x in self.rls:
                for y in self.rls:
                    for row in range(3 * x + 1, 3 * x + 4):
                        for col in range(3 * y + 1, 3 * y + 4):
                            for i in range(3 * x + 1, 3 * x + 4):
                                for j in range(3 * y + 1, 3 * y + 4):
                                    if i == row and j == col:
                                        continue
                                    clauses.append('-' + vals_to_clause(row, col, value) +
                                                   ' -' + vals_to_clause(i, j, value) + ' 0')

        # present entries
        for i in self.rlb:
            for j in self.rlb:
                num = self.sudoku[i][j][0]
                if num > 0:
                    clauses.append(vals_to_clause(i+1, j+1, num) + ' 0')

        with open(self.task + '.cnf', 'w') as file_cnf:
            file_cnf.write('p cnf ' + str(self.num_vars) + ' ' + str(len(clauses)) + '\n')
            file_cnf.write('\n'.join(clauses))

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
                    if int(elem) > 110:
                        relevant.append(elem)

        # fill solution sudoku
        for elem in relevant:
            self.sudoku[int(elem[0]) - 1][int(elem[1]) - 1][0] = int(elem[2])

    def create_solution(self):
        """Parse sudoku array and return a printable representation with information from original task.

        INDEPENDENT OF ENCODING
        """

        # task information
        sol = ['\n'.join(self.problem_description)]
        # fill solution string
        delimiter_row = self.small_size * ('+-' + ('-' * (self.small_size * (self.chars_per_number + 1)))) + '+'
        sol.append(delimiter_row)
        for line_number, line in enumerate(self.sudoku):
            linestring = '| '
            for column_number, column in enumerate(line):
                linestring += str(column[0]).rjust(self.chars_per_number) + ' '
                if column_number % self.small_size == (self.small_size - 1):
                    linestring += '| '
            sol.append(linestring)
            if line_number % self.small_size == (self.small_size - 1):
                sol.append(delimiter_row)

        with open(self.task + '_solution.txt', 'w') as file_solution:
            file_solution.write('\n'.join(sol))

        print('\n'.join(sol))

    def set_number_and_eliminate(self, num, i, j):
        """Set the number at the given coordinates to the given number and eliminate possibilities."""
        # set number
        self.sudoku[i][j][0] = num
        # no other possibilities where we set a number
        self.sudoku[i][j][1].clear()
        # eliminate possibilities in columns, lines and blocks
        for k in self.rlb:
            self.sudoku[k][j][1].discard(num)  # column
            self.sudoku[i][k][1].discard(num)  # line
        line_offset = (i // self.small_size) * self.small_size
        column_offset = (j // self.small_size) * self.small_size
        for l in self.rls:
            for m in self.rls:
                self.sudoku[line_offset + l][column_offset + m][1].discard(num)  # block


if __name__ == '__main__':
    # for interactive debugging
    s = Solver()
