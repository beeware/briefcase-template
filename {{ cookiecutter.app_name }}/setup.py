#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages
import sys

with io.open('./{{ cookiecutter.app_name }}/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='{{ cookiecutter.app_name }}',
    version=version,
    description='{{ cookiecutter.description }}',
    long_description=long_description,
    author='{{ cookiecutter.author }}',
    author_email='{{ cookiecutter.author_email }}',
    license='{{ cookiecutter.license }}',
    packages=find_packages(
        exclude=[
            'docs', 'tests',
            'windows', 'macOS', 'linux',
            'iOS', 'android',
            'django'
        ]
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: {{ cookiecutter.license }}',
    ],
    install_requires=[{% if cookiecutter.gui_framework == 'PySide2' %}
        'pyside2==5.13.0',{% endif %}
    ],
    options={
        'app': {
            'formal_name': '{{ cookiecutter.formal_name }}',
            'bundle': '{{ cookiecutter.bundle }}'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [{% if cookiecutter.gui_framework == 'Toga' %}
                'toga-cocoa==0.3.0.dev11',{% endif %}
            ]
        },
        'linux': {
            'app_requires': [{% if cookiecutter.gui_framework == 'Toga' %}
                'toga-gtk==0.3.0.dev11',{% endif %}
            ]
        },
        'windows': {
            'app_requires': [{% if cookiecutter.gui_framework == 'Toga' %}
                'toga-winforms==0.3.0.dev11',{% endif %}
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [{% if cookiecutter.gui_framework == 'Toga' %}
                'toga-ios==0.3.0.dev11',{% endif %}
            ]
        },
        'android': {
            'app_requires': [{% if cookiecutter.gui_framework == 'Toga' %}
                'toga-android==0.3.0.dev11',{% endif %}
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [{% if cookiecutter.gui_framework == 'Toga' %}
                'toga-django==0.3.0.dev11',{% endif %}
            ]
        },
    }
)
