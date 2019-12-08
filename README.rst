Briefcase Bootstrap template
============================

A template for starting a Python app that will be deployed using briefcase.

Using this template
-------------------

1. Install `cookiecutter`_. This is a tool used to bootstrap complex project
   templates::

    $ pip install cookiecutter

2. Run ``cookiecutter`` on this template::

    $ cookiecutter https://github.com/beeware/briefcase-template

3. Add your code to the project.

4. Install `Briefcase`_. This is the tool that will produce a version of your
   project that can be deployed to specific platforms::

    $ pip install briefcase

5. Use Briefcase to generate a project::

    $ briefcase create
    $ briefcase run

   To build for a mobile platform, add the platform name::

    $ briefcase create iOS
    $ briefcase run iOS

.. _cookiecutter: http://github.com/cookiecutter/cookiecutter
.. _briefcase: http://github.com/beeware/briefcase
