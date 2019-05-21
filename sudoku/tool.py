import os
import subprocess
import sys
from pathlib import Path

from reprobench.tools.executable import ExecutableTool
from reprobench.utils import download_file, extract_tar, extract_zip

DIR = Path(os.path.dirname(__file__))


def get_platform():
    if sys.platform.startswith("linux"):
        return "linux-x86_64"
    elif sys.platform.startswith("darwin"):
        return "macos-x86_64"
    elif sys.platform.startswith("win32"):
        return "win64"
    return None


class SudokuSatSolver(ExecutableTool):
    name = "My Sudoku SAT Solver"
    download_path = DIR / "_downloaded"

    clasp_dir = download_path / "clingo"
    clasp_path = clasp_dir / "clasp"

    riss_dir = download_path / "riss"
    riss_path = riss_dir / "bin" / "riss"

    glucose_dir = download_path / "glucose"
    glucose_path = glucose_dir / "simp" / "glucose"

    @classmethod
    def _setup_clasp(cls, platform):
        url = f"https://github.com/potassco/clingo/releases/download/v5.3.0/clingo-5.3.0-{platform}.tar.gz"
        destination = cls.download_path / "clingo-5.3.0.tar.gz"
        download_file(url, destination)
        extract_tar(destination, cls.clasp_dir)

    @classmethod
    def _setup_riss(cls):
        url = "http://tools.computational-logic.org/content/riss/riss_505.zip"
        destination = cls.download_path / "riss-5.0.5.zip"
        download_file(url, destination)
        extract_zip(destination, cls.riss_dir)

    # @classmethod
    # def _setup_glucose(cls):
    #     url = (
    #         "http://www.labri.fr/perso/lsimon/downloads/softwares/glucose-syrup-4.1.tgz"
    #     )
    #     destination = cls.download_path / "glucose-4.1.tar.gz"
    #     download_file(url, destination)
    #     extract_tar(destination, cls.glucose_dir)
    #     make_path = cls.glucose_dir / "simp"
    #     subprocess.run(["make"], cwd=make_path, shell=True)

    @classmethod
    def setup(cls):
        platform = get_platform()
        cls.download_path.mkdir(parents=True, exist_ok=True)

        cls._setup_clasp(platform)

        if platform == "linux-x86_64":
            #cls._setup_glucose()
            cls._setup_riss()

    @classmethod
    def is_ready(cls):
        platform = get_platform()

        if not cls.clasp_path.exists():
            return False

        if platform == "linux-x86_64":
            if not cls.riss_path.exists():
                return False
            if not cls.glucose_path.exists():
                return False

        return True
