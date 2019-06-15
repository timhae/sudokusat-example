#!/usr/env/bin python3

import math


def read_sudoku(filename):
    '''Parse input file and return a two-dimensional array for internal
    representation.
    '''

    # read file
    with open(filename) as f:
        entire_file = f.readlines()

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
        for (j, character) in enumerate(clean_line):
            if character == '_' or character == '__' or character == '___':
                sudoku_array[i][j] = 0
            else:
                sudoku_array[i][j] = int(character)

    return sudoku_array


#def write_sudoku(sudoku):
#    '''Parse sudoku array and return a printable representation.'''
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

