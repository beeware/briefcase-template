import os
import shutil

from cookiecutter import main
from flake8.api import legacy as flake8
import py_compile
import pytest
import tomlkit


@pytest.fixture(scope="session")
def app_directory(tmpdir_factory):
    """Fixture for a default app."""
    output_dir = str(tmpdir_factory.mktemp("default-app"))
    CCDS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    main.cookiecutter(
        str(CCDS_ROOT), no_input=True, output_dir=output_dir,
    )
    yield output_dir

    # cleanup after
    shutil.rmtree(output_dir)


def _all_filenames(directory):
    """Return list of filenames in a directory, excluding __pycache__ files."""
    filenames = []
    for root, _, files in os.walk(directory):
        for f in files:
            if "__pycache__" not in os.path.join(root, f):
                filenames.append(os.path.join(root, f))
    filenames.sort()
    return filenames


def test_parse_pyproject_toml(app_directory):
    """Test for erros in parsing the generated pyproject.toml file."""
    pyproject_toml = app_directory + os.sep + "helloworld" + os.sep + "pyproject.toml"
    assert os.path.exists(pyproject_toml)
    with open(pyproject_toml) as f:
        content = f.read()
    tomlkit.parse(content)  # any error in parsing will trigger pytest


def test_output_file_structure(app_directory):
    """Check the file tree structure generated is what we expect to see."""
    expected = [
        "helloworld" + os.sep + "LICENSE",
        "helloworld" + os.sep + "pyproject.toml",
        "helloworld" + os.sep + ".gitignore",
        "helloworld" + os.sep + "README.rst",
        "helloworld" + os.sep + "src" + os.sep + "helloworld" + os.sep + "__init__.py",
        "helloworld" + os.sep + "src" + os.sep + "helloworld" + os.sep + "app.py",
        "helloworld" + os.sep + "src" + os.sep + "helloworld" + os.sep + "__main__.py",
        "helloworld"
        + os.sep
        + "src"
        + os.sep
        + "helloworld"
        + os.sep
        + "resources"
        + os.sep
        + "helloworld.png",
        "helloworld"
        + os.sep
        + "src"
        + os.sep
        + "helloworld"
        + os.sep
        + "resources"
        + os.sep
        + "__init__.py",
        "helloworld"
        + os.sep
        + "src"
        + os.sep
        + "helloworld"
        + os.sep
        + "resources"
        + os.sep
        + "helloworld.ico",
        "helloworld"
        + os.sep
        + "src"
        + os.sep
        + "helloworld"
        + os.sep
        + "resources"
        + os.sep
        + "helloworld.icns",
    ]
    expected = [os.path.join(str(app_directory), f) for f in expected]
    expected.sort()
    output = _all_filenames(app_directory)
    assert output == expected


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
