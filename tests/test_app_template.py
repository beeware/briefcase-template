import py_compile
import subprocess
from pathlib import Path

import pytest
import toml
from cookiecutter import main

BASIC_APP_CONTEXT = {
    "formal_name": "Hello World",
    "app_name": "{{ cookiecutter.formal_name|lower|replace(' ', '') }}",
    "class_name": (
        "{{ cookiecutter.formal_name.title().replace(' ','').replace('-','')"
        ".replace('!','').replace('.','').replace(',','') }}"
    ),
    "module_name": "{{ cookiecutter.app_name|lower|replace('-', '_') }}",
    "project_name": "Project Awesome",
    "description": "An app that does lots of stuff",
    "author": "Jane Developer",
    "author_email": "jane@example.com",
    "bundle": "com.example",
    "url": "https://example.com",
    "license": "BSD-3-Clause",
    "test_framework": "pytest",
}

SIMPLE_TABLE_CONTENT = """\
requires = [
    "{}==1.1.0",
]
"""

APP_SOURCE = """\
from datetime import datetime


def main():
    print(f"hello world - it's {datetime.utc()}")
"""

APP_START_SOURCE = """\
from .app import app

if __name__ == "__main__":
    app()
"""

TEST_CASES = [
    pytest.param(
        BASIC_APP_CONTEXT,
        '''\
# This project was generated with Unknown using template: Not provided @ Not provided
[tool.briefcase]
project_name = "Project Awesome"
bundle = "com.example"
version = "0.0.1"
url = "https://example.com"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
author = "Jane Developer"
author_email = "jane@example.com"

[tool.briefcase.app.helloworld]
formal_name = "Hello World"
description = "An app that does lots of stuff"
long_description = """More details about the app should go here.
"""
sources = [
    "src/helloworld",
]
test_sources = [
    "tests",
]

''',
        id="minimum-context",
    ),
    pytest.param(
        {
            **BASIC_APP_CONTEXT,
            "test_framework": "unittest",
            "app_source": APP_SOURCE,
            "app_start_source": APP_START_SOURCE,
            "pyproject_table_macOS": SIMPLE_TABLE_CONTENT.format("macOS"),
            "pyproject_table_linux": SIMPLE_TABLE_CONTENT.format("linux"),
            "pyproject_table_linux_system_debian": SIMPLE_TABLE_CONTENT.format("deb"),
            "pyproject_table_linux_system_rhel": SIMPLE_TABLE_CONTENT.format("rhel"),
            "pyproject_table_linux_system_suse": SIMPLE_TABLE_CONTENT.format("suse"),
            "pyproject_table_linux_system_arch": SIMPLE_TABLE_CONTENT.format("arch"),
            "pyproject_table_linux_appimage": SIMPLE_TABLE_CONTENT.format("appimage"),
            "pyproject_table_linux_flatpak": SIMPLE_TABLE_CONTENT.format("flatpak"),
            "pyproject_table_windows": SIMPLE_TABLE_CONTENT.format("windows"),
            "pyproject_table_iOS": SIMPLE_TABLE_CONTENT.format("iOS"),
            "pyproject_table_android": SIMPLE_TABLE_CONTENT.format("android"),
            "pyproject_table_web": SIMPLE_TABLE_CONTENT.format("web"),
            "briefcase_version": "v0.3.16-2",
            "template_source": "https://example.com/beeware/briefcase-template",
            "template_branch": "my-branch",
        },
        '''\
# This project was generated with v0.X.Y using template: a/b @ my-branch
[tool.briefcase]
project_name = "Project Awesome"
bundle = "com.example"
version = "0.0.1"
url = "https://example.com"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
author = "Jane Developer"
author_email = "jane@example.com"

[tool.briefcase.app.helloworld]
formal_name = "Hello World"
description = "An app that does lots of stuff"
long_description = """More details about the app should go here.
"""
sources = [
    "src/helloworld",
]
test_sources = [
    "tests",
]

[tool.briefcase.app.helloworld.macOS]
requires = [
    "macOS==1.1.0",
]

[tool.briefcase.app.helloworld.linux]
requires = [
    "linux==1.1.0",
]

[tool.briefcase.app.helloworld.linux.system.debian]
requires = [
    "deb==1.1.0",
]

[tool.briefcase.app.helloworld.linux.system.rhel]
requires = [
    "rhel==1.1.0",
]

[tool.briefcase.app.helloworld.linux.system.suse]
requires = [
    "suse==1.1.0",
]

[tool.briefcase.app.helloworld.linux.system.arch]
requires = [
    "arch==1.1.0",
]

[tool.briefcase.app.helloworld.linux.appimage]
requires = [
    "appimage==1.1.0",
]

[tool.briefcase.app.helloworld.linux.flatpak]
requires = [
    "flatpak==1.1.0",
]

[tool.briefcase.app.helloworld.windows]
requires = [
    "windows==1.1.0",
]

# Mobile deployments
[tool.briefcase.app.helloworld.iOS]
requires = [
    "iOS==1.1.0",
]

[tool.briefcase.app.helloworld.android]
requires = [
    "android==1.1.0",
]

# Web deployments
[tool.briefcase.app.helloworld.web]
requires = [
    "web==1.1.0",
]

''',
        id="normal-context",
    ),
    pytest.param(
        {
            **BASIC_APP_CONTEXT,
            "app_source": APP_SOURCE,
            "app_start_source": APP_START_SOURCE,
            "pyproject_table_briefcase_extra_content": """
field = "pyproject_table_briefcase_extra_content"
answer = 42
""",
            "pyproject_table_briefcase_app_extra_content": """
other_resources = [
    "dir",
    "otherdir",
    "pyproject_table_briefcase_app_extra_content",
]
""",
            "pyproject_table_macOS": SIMPLE_TABLE_CONTENT.format("macOS"),
            "pyproject_table_linux": SIMPLE_TABLE_CONTENT.format("linux"),
            "pyproject_table_linux_appimage": SIMPLE_TABLE_CONTENT.format("appimage"),
            "pyproject_table_linux_flatpak": SIMPLE_TABLE_CONTENT.format("flatpak"),
            "pyproject_table_windows": SIMPLE_TABLE_CONTENT.format("windows"),
            "pyproject_table_iOS": SIMPLE_TABLE_CONTENT.format("iOS"),
            "pyproject_table_android": SIMPLE_TABLE_CONTENT.format("android"),
            "pyproject_extra_content": """\
[tool.briefcase.{{ cookiecutter.app_name|escape_non_ascii }}.my_custom_format_one]
field = "pyproject_extra_content"

nested_table = { "answer" = 42, "field" = "asdf" }

[tool.briefcase.{{ cookiecutter.app_name|escape_non_ascii }}.my_custom_format_two]
list = [
    "value",
    "value",
]
""",
            "briefcase_version": "v0.3.16-3",
            "template_source": "https://example.com/beeware/briefcase-template",
            "template_branch": "my-branch",
        },
        '''\
# This project was generated with v0.X.Y using template: a/b @ my-branch
[tool.briefcase]
project_name = "Project Awesome"
bundle = "com.example"
version = "0.0.1"
url = "https://example.com"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
author = "Jane Developer"
author_email = "jane@example.com"

field = "pyproject_table_briefcase_extra_content"
answer = 42

[tool.briefcase.app.helloworld]
formal_name = "Hello World"
description = "An app that does lots of stuff"
long_description = """More details about the app should go here.
"""
sources = [
    "src/helloworld",
]
test_sources = [
    "tests",
]

other_resources = [
    "dir",
    "otherdir",
    "pyproject_table_briefcase_app_extra_content",
]

[tool.briefcase.app.helloworld.macOS]
requires = [
    "macOS==1.1.0",
]

[tool.briefcase.app.helloworld.linux]
requires = [
    "linux==1.1.0",
]

[tool.briefcase.app.helloworld.linux.appimage]
requires = [
    "appimage==1.1.0",
]

[tool.briefcase.app.helloworld.linux.flatpak]
requires = [
    "flatpak==1.1.0",
]

[tool.briefcase.app.helloworld.windows]
requires = [
    "windows==1.1.0",
]

# Mobile deployments
[tool.briefcase.app.helloworld.iOS]
requires = [
    "iOS==1.1.0",
]

[tool.briefcase.app.helloworld.android]
requires = [
    "android==1.1.0",
]

[tool.briefcase.helloworld.my_custom_format_one]
field = "pyproject_extra_content"

nested_table = { "answer" = 42, "field" = "asdf" }

[tool.briefcase.helloworld.my_custom_format_two]
list = [
    "value",
    "value",
]
''',
        id="normal-context-with-extra-content",
    ),
    pytest.param(
        {
            **BASIC_APP_CONTEXT,
            "app_source": APP_SOURCE,
            "app_start_source": APP_START_SOURCE,
            "pyproject_table_briefcase_extra_content": (
                'field = "pyproject_table_briefcase_extra_content"\n'
            ),
            "pyproject_table_briefcase_app_extra_content": """
other_resources = ["dir", "pyproject_table_briefcase_app_extra_content"]
""",
            "pyproject_extra_content": """\
[tool.briefcase.{{ cookiecutter.app_name|escape_non_ascii }}.my_custom_format_one]
field = "pyproject_extra_content_one"

[tool.briefcase.{{ cookiecutter.app_name|escape_non_ascii }}.my_custom_format_two]
field = "pyproject_extra_content_two"

""",
            "briefcase_version": "v0.3.16-3",
            "template_source": "https://example.com/beeware/briefcase-template",
            "template_branch": "my-branch",
        },
        '''\
# This project was generated with v0.X.Y using template: a/b @ my-branch
[tool.briefcase]
project_name = "Project Awesome"
bundle = "com.example"
version = "0.0.1"
url = "https://example.com"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
author = "Jane Developer"
author_email = "jane@example.com"
field = "pyproject_table_briefcase_extra_content"

[tool.briefcase.app.helloworld]
formal_name = "Hello World"
description = "An app that does lots of stuff"
long_description = """More details about the app should go here.
"""
sources = [
    "src/helloworld",
]
test_sources = [
    "tests",
]

other_resources = ["dir", "pyproject_table_briefcase_app_extra_content"]

[tool.briefcase.helloworld.my_custom_format_one]
field = "pyproject_extra_content_one"

[tool.briefcase.helloworld.my_custom_format_two]
field = "pyproject_extra_content_two"

''',
        id="only-extra-content",
    ),
]


@pytest.fixture
def app_directory(tmp_path, context):
    """Fixture for a default app."""
    main.cookiecutter(
        str(Path(__file__).parent.parent.resolve()),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context=context,
    )
    return tmp_path


@pytest.mark.parametrize(("context", "expected_toml"), TEST_CASES)
def test_parse_pyproject_toml(app_directory, context, expected_toml):
    """Test for errors in parsing the generated pyproject.toml file."""
    pyproject_toml = app_directory / "helloworld" / "pyproject.toml"
    assert pyproject_toml.is_file()  # check pyproject.toml exists
    toml.load(pyproject_toml)  # any error in parsing will trigger pytest failure
    assert expected_toml == pyproject_toml.read_text()


@pytest.mark.parametrize(("context", "expected_toml"), TEST_CASES)
def test_ruff(app_directory, context, expected_toml):
    """Check there are no ruff errors in any of the generated python files."""
    try:
        subprocess.run(["ruff", "check", app_directory], check=True)
    except subprocess.CalledProcessError:
        pytest.fail("Ruff found style violations")

    try:
        subprocess.run(["ruff", "format", app_directory], check=True)
    except subprocess.CalledProcessError:
        pytest.fail("Ruff found format violations")


@pytest.mark.parametrize(("context", "expected_toml"), TEST_CASES)
def test_files_compile(app_directory, context, expected_toml):
    for filename in app_directory.glob("**/*.py"):
        # If there is a compilation error, pytest is triggered
        py_compile.compile(str(filename))
