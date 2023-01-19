{%- if cookiecutter.test_framework == 'pytest' -%}
import os
import tempfile
from pathlib import Path

import pytest


def run_tests():
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)
    returncode = pytest.main(
        [
            # Turn up verbosity
            "-vv",
            # Disable color
            "--color=no",
            # Overwrite the cache directory to somewhere writable
            "-o",
            f"cache_dir={tempfile.gettempdir()}/.pytest_cache",
            project_path / "tests"
        ]
    )
{%- elif cookiecutter.test_framework == "unittest" -%}
import os
import unittest
from pathlib import Path


def run_tests():
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)
    loader = unittest.TestLoader()
    suite = loader.discover(project_path / "tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    returncode = int(not result.wasSuccessful())
{%- endif %}

    print(f">>>>>>>>>> EXIT {returncode} <<<<<<<<<<")


if __name__ == "__main__":
    run_tests()
