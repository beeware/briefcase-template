Briefcase Bootstrap template
============================

A template for starting a Python app that will be deployed using briefcase.

Using this template
-------------------

1. Install `cookiecutter`_. This is a tool used to bootstrap complex project
   templates::

    $ pip install cookiecutter

2. Run ``cookiecutter`` on the Python-Linux template::

    $ cookiecutter https://github.com/pybee/briefcase-template

3. Add your code to the project.

4. Install `Briefcase`_. This is the tool that will produce a version of your
   project that can be deployed to specific platforms::

    $ pip install briefcase

5. Use Briefcase to generate the artefacts for your platform of choice::

    $ python setup.py ios
    $ python setup.py android
    $ python setup.py macos
    $ python setup.py windows
    $ python setup.py linux

.. _cookiecutter: http://github.com/audreyr/cookiecutter
.. _briefcase: http://github.com/pybee/briefcase
