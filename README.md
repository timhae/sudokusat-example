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

### Running the benchmark

```sh
(env) $ reprobench server &
(env) $ reprobench bootstrap
(env) $ reprobench manage local run
(env) $ fg
# Stop the server (Ctrl + C)
^C
```

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
