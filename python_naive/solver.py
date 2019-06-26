#!/usr/env/bin python3

import argparse
import math
import subprocess


def read_sudoku(filename):
    '''Parse input file and return a two-dimensional array for internal
    representation.

    INDEPENDENT OF ENCODING
    '''

    # read file
    with open(filename) as file_input:
        entire_file = file_input.readlines()

    # get puzzle size, assume it is always in line 3
    size = int(entire_file[3].split()[2].split('x')[0])
    small_size = int(math.sqrt(size))

    # select relevant lines (no divider lines)
    sudoku = [line for (i, line) in enumerate(entire_file[4:]) if i % (small_size + 1) != 0]

    # create and fill array
    sudoku_array = [[0 for _ in range(size)] for _ in range(size)]
    for (i, line) in enumerate(sudoku):
        # filter '|' characters
        clean_line = [c for (i, c) in enumerate(line.split()) if i % (small_size + 1) != 0]
        for (j, number) in enumerate(clean_line):
            if '_' in number:
                sudoku_array[i][j] = 0
            else:
                sudoku_array[i][j] = int(number)

    return sudoku_array


#def write_sudoku(sudoku):
#    '''Parse sudoku array and return a printable representation.
#
#    INDEPENDENT OF ENCODING
#    '''
#
#    # get puzzle size
#    size = len(sudoku[0])
#    small_size = int(math.sqrt(size))
#    chars_per_number = len(str(size))
#
#    # fill array
#    sudoku_array = [[0 for _ in range(size)] for _ in range(size)]
#    for (i, line) in enumerate(sudoku):
#        # filter '|' characters
#        clean_line = [c for (i, c) in enumerate(line.split(' ')) if i % (small_size + 1) != 0]
#        for (j, character) in enumerate(clean_line):
#            if ord(character) == 95:  # '_' character
#                sudoku_array[i][j] = 0
#            else:
#                sudoku_array[i][j] = int(character)
#
#    return sudoku_array


def input_to_cnf(filename_task):
    '''Read input and create cnf.

    ENCODING DEPENDENT
    '''
    pass #use read_sudoku

def solver_to_output(filename_solution):
    '''Read solver output and create complete sudoku.

    ENCODING DEPENDENT
    '''
    pass #use write_sudoku


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create constraint files for sudoku solvers.')
    parser.add_argument('solver', help='The solver to use.')
    parser.add_argument('task', help='Filepath of the problem description to solve.')
    args = parser.parse_args()
    filename_base = '.'.join(args.task.split('.')[0:-1])

    # create the cnf out of the input
    cnf = input_to_cnf(args.task)
    with open(filename_base + '.cnf', 'w') as file_cnf:
        file_cnf.write(cnf)

    # solve the cnf with the given solver and store result
    with open(filename_base + '.sol', 'w') as file_solved:
        subprocess.run([args.solver, filename_base + '.cnf'], STDOUT=file_solved)

    # create the solution with the help of the solver output
    solution = solver_to_output(filename_base + '.sol')
    with open(filename_base + '_solution.txt', 'w') as file_solution:
        file_solution.write(solution)

