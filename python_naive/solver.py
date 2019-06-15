#!/usr/env/bin python3

import argparse
import subprocess


parser = argparse.ArgumentParser(description='Create constraint files for sudoku solvers.')
parser.add_argument('solver', help='The solver to use.')
parser.add_argument('task', help='Filepath of the problem description to solve.')
args = parser.parse_args()


def in_to_cnf(task):
    """read input and create cnf"""
    with open(task) as f:
        sudoku_in = f.readlines()


def sol_to_out(task):
    """read solver output and create complete sudoku"""
    with open(task) as f:
        pass


# create the cnf out of the input
cnf = in_to_cnf(args.task)
with open(args.task + '.cnf', 'w') as file_cnf:
    file_cnf.write(cnf)

# solve the cnf with the given solver
with open(args.task + '_solved.cnf') as file_cnf_solved:
    subprocess.run([args.solver, args.task + '.cnf'], STDOUT=file_cnf_solved)

# create the solution with the help of the solved formula
with open(args.task
sol = sol_to_out(cnf_solved)
with open(args.task '.sol', 'w') as file_solution:
    file_solution.write(

