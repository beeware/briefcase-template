import pathlib
import shutil

from cookiecutter import main
from flake8.api import legacy as flake8
import py_compile
import pytest
import toml

TEST_CASES = [
    {},  # use only the default briefcase-template values
    # GUI framework options
    {"gui_framework": "1"},  # Toga GUI framework
    {"gui_framework": "2"},  # PySide2 GUI framework
    {"gui_framework": "3"},  # PySide6 GUI framework
    {"gui_framework": "4"},  # PursuedPyBear GUI framework
    {"gui_framework": "5"},  # "None" for GUI framework
    # Test framework options
    {"test_framework": "1"},  # pytest test framework
    {"test_framework": "2"},  # unittest test framework
]


@pytest.fixture
def app_directory(tmpdir_factory, args):
    """Fixture for a default app."""
    output_dir = tmpdir_factory.mktemp("default-app")
    output_dir = pathlib.Path(str(output_dir)).resolve()
    root_dir = pathlib.Path(__file__).parent.parent.resolve()
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


@pytest.mark.parametrize('args', TEST_CASES)
def test_parse_pyproject_toml(app_directory):
    """Test for errors in parsing the generated pyproject.toml file."""
    pyproject_toml = app_directory / "helloworld" / "pyproject.toml"
    assert pyproject_toml.is_file()  # check pyproject.toml exists
    toml.load(pyproject_toml)  # any error in parsing will trigger pytest


@pytest.mark.parametrize('args', TEST_CASES)
def test_flake8_app(app_directory, args):
    """Check there are no flake8 errors in any of the generated python files"""
    files = [f for f in _all_filenames(app_directory) if f.endswith(".py")]
    style_guide = flake8.get_style_guide()
    report = style_guide.check_files(files)
    assert report.get_statistics("E") == [], "Flake8 found violations"


@pytest.mark.parametrize('args', TEST_CASES)
def test_files_compile(app_directory, args):
    files = [f for f in _all_filenames(app_directory) if f.endswith(".py")]
    for filename in files:
        # If there is a compilation error, pytest is triggered
        py_compile.compile(filename)
