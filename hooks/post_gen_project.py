import os
import sys

REMOVE_PATHS = [
    '{% if cookiecutter.gui_framework != "PositronDjango" %} {{ cookiecutter.app_name }}/src/webapp/ {% endif %}',
    '{% if cookiecutter.gui_framework != "PositronStatic" %} {{ cookiecutter.app_name }}/src/{{ cookiecutter.module_name }}/resources/webapp/ {% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.unlink(path)
