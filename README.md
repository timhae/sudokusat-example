# Sudoku SAT

Please fork this repository and add your own solver implementation accordingly.
You can run the sample benchmark with the following instruction.

## Benchmarking with [reprobench](https://github.com/rkkautsar/reprobench)

### Installation

Python 3 is used here. One can use [pyenv](#using-pyenv) to install this Python version.

```sh
# setup a virtualenv
$ python -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
# make sure reprobench is installed
(env) $ reprobench --version
```

### Writing the tool interface

Modify [`my_solver/__init__.py`](my_solver/__init__.py).
Further instructions is provided in the relevant files.

You can also modify the solver name by renaming the folder.
If you do this, you have to change the relevant line in [`benchmark.yml`](benchmark.yml).
It is also possible to add more than one solver to the benchmark, for example to compare with your own alternative algorithms or others' solvers.

By default the benchmark tool will run my_solver/my_solver.sh.
See details there.

### Running the benchmark

```sh
(env) $ reprobench server &             # run the server in background
(env) $ reprobench bootstrap && reprobench manage local run
(env) $ fg                              # bring the server back to foreground
# Stop the server (Ctrl + C)
^C
```

### Check output
The benchmark tool generates under "output" a folder for each solver, then a folder for each parameter (SAT solver), and then under sudoku a folder for each benchmark instance.

As example we placed:
output/my_solver.MySudokuSolver/clasp/sudoku/bsp-sudoku1.txt

Then our tool "my_solver.sh" will alwasy output the example solution given in "bsp-sudoku1.sol" if it detects "bsp-sudoku1.txt" as input instance into the file run.out.
This file will afterwards be checked by the validator.

You can check the validation (you might have to install sqlite3 on windows):

```bash
(env) vagrant@debian:~/sudokusat-example$ sqlite3 output/benchmark.db 
SQLite version 3.27.2 2019-02-25 16:06:06
Enter ".help" for usage hints.
sqlite> select * from sudokuverdict;

1|1|0
2|2|0
3|3|0
4|4|0
5|5|0
6|6|0
7|7|0
8|8|0
9|9|0
10|10|0
11|11|0
12|12|0
13|13|0
14|14|0
15|15|0
16|16|0
17|17|0
18|18|0
19|19|0
20|20|0
21|21|0
22|22|0
23|23|0
24|24|0
25|25|0
26|26|0
27|27|0
28|28|1
29|29|0
30|30|0
31|31|0
32|32|0
sqlite> 
```
(later we will probably provide a command with reprobench analyze that does the trick)


### Analysis

```sh
(env) $ reprobench analyze
```

Then open the resulting `output/statistics/summary.csv` file.

---

## Appendix

### Using `pyenv`

`pyenv` is a Python version manager to allow one to install and use different python versions across projects.

- Install pyenv, refer to [pyenv-installer](https://github.com/pyenv/pyenv-installer).
- Install Python 3. For example: `pyenv install 3.7.2`
- Use the installed Python version: `pyenv global 3.7.2` (or `pyenv local 3.7.2`, if preferred)
