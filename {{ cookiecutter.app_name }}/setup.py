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
    packages=find_packages(exclude=['docs', 'tests']),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: {{ cookiecutter.license }}',
    ],
    install_requires=[
    ],
    options={
        'app': {
            'formal_name': '{{ cookiecutter.formal_name }}',
            'bundle': '{{ cookiecutter.bundle }}'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [
            ]
        },
        'linux': {
            'app_requires': [
            ]
        },
        'windows': {
            'app_requires': [
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
            ]
        },
        'android': {
            'app_requires': [
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
            ]
        },
    }
)
