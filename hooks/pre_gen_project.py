import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

app_name = '{{ cookiecutter.app_name }}'

if not re.match(MODULE_REGEX, app_name):
    print('ERROR: `%s` is not a valid Python module name!' % app_name)

    # exits with status 1 to indicate failure
    sys.exit(1)
