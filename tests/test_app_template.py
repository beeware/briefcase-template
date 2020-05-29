import pathlib
import shutil

from cookiecutter import main
from flake8.api import legacy as flake8
import py_compile
import pytest
import toml


@pytest.fixture(scope="session")
def app_directory(tmpdir_factory):
    """Fixture for a default app."""
    output_dir = tmpdir_factory.mktemp("default-app")
    output_dir = pathlib.Path(str(output_dir)).resolve()
    root_dir = pathlib.Path(__file__).parents[1].resolve()
    main.cookiecutter(
        str(root_dir), no_input=True, output_dir=str(output_dir),
    )
    return output_dir


def _all_filenames(directory):
    """Return list of filenames in a directory, excluding __pycache__ files."""
    filenames = []
    for root, _, files in pathlib.os.walk(str(directory)):
        for f in files:
            full_filename = root+pathlib.os.sep+f
            if "__pycache__" not in full_filename:
                filenames.append(full_filename)
    filenames.sort()
    return filenames


def test_parse_pyproject_toml(app_directory):
    """Test for errors in parsing the generated pyproject.toml file."""
    pyproject_toml = app_directory/"helloworld"/"pyproject.toml"
    assert pyproject_toml.is_file()  # check pyproject.toml exists
    toml.load(pyproject_toml)  # any error in parsing will trigger pytest


def test_flake8_app(app_directory):
    """Check there are no flake8 errors in any of the generated python files"""
    files = [f for f in _all_filenames(app_directory) if f.endswith(".py")]
    style_guide = flake8.get_style_guide()
    report = style_guide.check_files(files)
    assert report.get_statistics("E") == [], "Flake8 found violations"


def test_files_compile(app_directory):
    files = [f for f in _all_filenames(app_directory) if f.endswith(".py")]
    for filename in files:
        # If there is a compilation error, pytest is triggered
        py_compile.compile(filename)
