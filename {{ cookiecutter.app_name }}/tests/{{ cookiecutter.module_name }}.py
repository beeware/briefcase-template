{%- if cookiecutter.test_framework == 'pytest' -%}
import os
import sys
import tempfile
from pathlib import Path

import pytest


def test_suite():
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)

    ##################################################################
    # WORKAROUND - On Android, we need to explicitly unpack the test
    # source code into a location where it can be discovered.
    ##################################################################
    if hasattr(sys, "getandroidapilevel"):
        import tests

        def chaquopy_extract_package(pkg):
            finder = pkg.__loader__.finder
            for path in pkg.__path__:
                chaquopy_extract_dir(finder, finder.zip_path(path))

        def chaquopy_extract_dir(finder, zip_dir):
            for filename in finder.listdir(zip_dir):
                zip_path = f"{zip_dir}/{filename}"
                if finder.isdir(zip_path):
                    chaquopy_extract_dir(finder, zip_path)
                else:
                    finder.extract_if_changed(zip_path)
        chaquopy_extract_package(tests)
    ##################################################################

    result = pytest.main(
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
import sys
import unittest
from pathlib import Path


def test_suite():
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)

    ##################################################################
    # WORKAROUND - On Android, we need to explicitly unpack the test
    # source code into a location where it can be discovered.
    ##################################################################
    if hasattr(sys, "getandroidapilevel"):
        import tests

        def chaquopy_extract_package(pkg):
            finder = pkg.__loader__.finder
            for path in pkg.__path__:
                chaquopy_extract_dir(finder, finder.zip_path(path))

        def chaquopy_extract_dir(finder, zip_dir):
            for filename in finder.listdir(zip_dir):
                zip_path = f"{zip_dir}/{filename}"
                if finder.isdir(zip_path):
                    chaquopy_extract_dir(finder, zip_path)
                else:
                    finder.extract_if_changed(zip_path)

        chaquopy_extract_package(tests)
    ##################################################################

    loader = unittest.TestLoader()
    suite = loader.discover(project_path / "tests")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
{%- endif %}


if __name__ == "__main__":
    test_suite()
